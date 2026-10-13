"""Prepare the speech and camera of a cut from the source recording.

Usage inside a cut's prepare.py:
    from prepare_cut import prepare_cut
    prepare_cut(SOURCE, WORK, BLOCKS, crop="crop=320:238:1548:412")   # or crop=None for the full frame

BLOCKS: list of (key, start, end, end_radius[, start_radius]) in seconds of the source. Boundaries snap to the
energy valley (10 ms windows) and to whole frames. The silence threshold is measured per recording:
noise floor (10th percentile of 10 ms RMS) + 12 dB, clamped to [-48, -32] dBFS. Internal pauses longer than
`min_pause` are shortened, keeping `edge` seconds on each side. Speed is always 1x (never speed up speech).
Outputs: composition/assets/camera-src.mp4, voice-raw.wav and edl.json.
"""

import json
import math
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000


def _pcm(source, start, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.4f}", "-t", f"{dur:.4f}", "-i", str(source),
                          "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "pipe:1"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def _rms10(x):
    hop = SR // 100
    f = x[: len(x) // hop * hop].reshape(-1, hop)
    return 20 * np.log10(np.sqrt(np.mean(f ** 2, axis=1)) + 1e-9)


def _quiet(source, t, radius):
    r = _rms10(_pcm(source, t - radius, 2 * radius))
    i = int(np.argmin(r))
    return t - radius + (i + 0.5) / 100, float(r[i])


def prepare_cut(source, work, blocks, crop, fps=24, min_pause=0.7, edge=0.18, tail_fade=0.04):
    source, work = Path(source), Path(work)
    assets = work / "composition/assets"
    assets.mkdir(parents=True, exist_ok=True)
    (work / "clips").mkdir(exist_ok=True)
    (work / "qa").mkdir(exist_ok=True)
    blocks = [tuple(bl) + (0.2,) * (5 - len(bl)) for bl in blocks]  # (chave, início, fim, raio_fim, raio_início)
    levels = np.concatenate([_rms10(_pcm(source, bl[1], bl[2] - bl[1])) for bl in blocks])
    floor = float(np.percentile(levels, 10))
    thr = min(-32.0, max(-48.0, floor + 12))
    voice, videos, chunks, trims, cursor = [], [], [], [], 0.0
    for g, (key, a, b, rb, ra) in enumerate(blocks):
        qa_, da = _quiet(source, a, ra)
        qb_, db_ = _quiet(source, b, rb)
        f0, f1 = round(qa_ * fps), math.floor(qb_ * fps + 1e-6)
        start, dur = f0 / fps, (f1 - f0) / fps
        x = _pcm(source, start, dur)
        n = round(dur * SR)
        x = np.pad(x[:n], (0, max(0, n - len(x))))
        lv = _rms10(x)
        quiet = lv < thr
        removed, i = [], 0
        while i < len(quiet):
            if quiet[i]:
                j = i
                while j < len(quiet) and quiet[j]:
                    j += 1
                s, e = i / 100, j / 100
                if e - s > min_pause and s > 0.1 and e < dur - 0.1:
                    r0, r1 = math.ceil((s + edge) * fps), math.floor((e - edge) * fps)
                    if r1 - r0 >= 1:
                        removed.append((r0, r1))
                        trims.append({"block": key, "source_start": start + s, "source_end": start + e,
                                      "removed_s": (r1 - r0) / fps})
                i = j
            else:
                i += 1
        keeps, pos = [], 0
        for r0, r1 in removed:
            keeps.append((pos, r0))
            pos = r1
        keeps.append((pos, f1 - f0))
        graph = ""
        for k, (k0, k1) in enumerate(keeps):
            seg = x[k0 * SR // fps: k1 * SR // fps].copy()
            r = round(0.004 * SR)
            seg[:r] *= np.linspace(0, 1, r)
            seg[-r:] *= np.linspace(1, 0, r)
            voice.append(seg)
            span = (k1 - k0) / fps
            chunks.append({"block": key, "source_in": start + k0 / fps, "source_out": start + k1 / fps,
                           "out_start": cursor, "out_end": cursor + span, "speed": 1.0})
            cursor += span
            graph += f"[0:v]trim=start_frame={k0}:end_frame={k1},setpts=PTS-STARTPTS[v{k}];"
        chunks[-1]["boundary_db"] = [round(da, 1), round(db_, 1)]
        graph += "".join(f"[v{k}]" for k in range(len(keeps))) + f"concat=n={len(keeps)}:v=1:a=0,format=yuv420p[v]"
        raw_clip, clip = work / "clips" / f"raw-{g}.mp4", work / "clips" / f"edited-{g}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.4f}", "-i", str(source), *(["-vf", crop] if crop else []), "-an",
                        "-frames:v", str(f1 - f0), "-r", str(fps), "-c:v", "libx264", "-crf", "14", "-preset", "fast",
                        str(raw_clip)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw_clip), "-filter_complex", graph, "-map", "[v]", "-an",
                        "-r", str(fps), "-c:v", "libx264", "-crf", "14", "-preset", "fast", str(clip)], check=True)
        videos.append(clip)
    lst = work / "clips/list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in videos))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(assets / "camera-src.mp4")], check=True)
    v = np.concatenate(voice)
    t = round(tail_fade * SR)
    v[-t:] *= np.linspace(1, 0, t)
    peak = float(np.max(np.abs(v)))
    if peak > 0.98:
        v *= 0.98 / peak
    with wave.open(str(assets / "voice-raw.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((v * 32767).astype("<i2").tobytes())
    edl = {"source": str(source), "fps": fps, "crop": crop, "speed": 1.0, "voice_duration": len(v) / SR,
           "noise_floor_dbfs": round(floor, 1), "silence_threshold_dbfs": round(thr, 1), "min_pause_s": min_pause,
           "chunks": chunks, "silence_trims": trims, "removed_seconds": sum(x["removed_s"] for x in trims)}
    (work / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=2))
    return edl
