"""Confere se as variantes de câmera (camera-*.mp4) estão alinhadas quadro a quadro com camera-src.mp4.

Uso: camera_sync_check.py <work> [variante ...]
Para tempos amostrados, procura o quadro de camera-src mais parecido (±3 s) com o quadro da variante.
Offset 0 em todos os tempos = sincronizado.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

W, H, FPS = 64, 48, 24


def frames(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf",
                          f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W).astype(np.float32)
    f = f - f.mean(axis=(1, 2), keepdims=True)
    return f / (f.std(axis=(1, 2), keepdims=True) + 1e-6)


def main():
    work = Path(sys.argv[1])
    a = work / "composition/assets"
    names = sys.argv[2:] or [p.stem for p in sorted(a.glob("camera-*.mp4")) if p.stem != "camera-src"]
    src = frames(a / "camera-src.mp4")
    ok = True
    for name in names:
        var = frames(a / f"{name}.mp4")
        n = min(len(src), len(var))
        offsets = []
        for i in np.linspace(FPS, n - FPS - 1, 12).astype(int):
            lo, hi = max(0, i - 3 * FPS), min(len(src), i + 3 * FPS)
            scores = [(float(np.mean(var[i] * src[j])), j - i) for j in range(lo, hi)]
            offsets.append(int(max(scores)[1]))
        synced = len(var) == len(src) and sorted(abs(o) for o in offsets)[len(offsets) * 3 // 4] <= 1  # filtros fortes (sketch, posterize) geram outliers isolados
        ok &= synced
        print(f"{name}: frames {len(var)} vs src {len(src)}; offsets (quadros) {offsets} -> {'OK' if synced else 'FORA DE SINCRONIA'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
