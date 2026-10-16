# Changelog

## Unreleased
- `heditor test` accepts long-form cuts: `plan["max_duration"]` (or `HEDITOR_MAX_DURATION`) raises the default 70 s limit up to 180 s, the Instagram Reels maximum.

## 1.6.1 — 2026-10-15
- `lousa-de-aula` approved after its first production and marked as a reusable style for technical explanations.

## 1.6.0 — 2026-10-15
- New didactic style `lousa-de-aula` (interactive chalkboard lesson): the whole screen is a classroom slate and the explanation is drawn live in chalk, each stroke starting on the word that triggers it (±0.15 s); numbered syllabus whose "?" turns into ✓, arrows labelled with the spoken verb, emphasis circles and double underlines, a felt eraser that wipes by mask, a SUMMARY board that rebuilds the chain, the teacher in a framed picture that shrinks to a corner and grows back, captions written on the board's margin, homework CTA. Full recipe: word-synced keys with `rk.finder`, pure `render(t)` engine, `stroke-dashoffset` drawing, hand jitter and double strokes, SVG chalk filter + grain mask, chalk stick and dust at the tip, handwriting reveal, eraser mask, per-stroke chalk SFX levels, `music:282` with the real drop at 12.45 s.
- troubleshooting.md: recipe "Drawing synced to speech" (sync keys, stroke offsets, consequence strokes, sync-table gate) and new rows for the cost of SVG filters in the render, small chalk labels, arrow-label agreement and an eraser that does not read as erasing.
- INDEX: new **didactic** family.

## 1.5.0 — 2026-10-15
- New `depthkit` module (`scripts/reelkit/depthkit.py`) for layered 2.5D/3D edits, every output frame for frame with `camera-hd.mp4` and rebuilt when stale:
  - `person_matte`: speaker alpha as `camera-alpha.webm` (camera RGB untouched) + `matte-person.mp4`, MediaPipe multiclass segmenter with temporal smoothing and a guided-filter edge, matte sheet and coverage stats for QA;
  - `depth_map` (Depth Anything V2 Small, ONNX, Apache-2.0) and `depth_look` (any ffmpeg grade on the far parts only, e.g. depth fog);
  - `edge_look` (room as glowing iso-depth contours or edge lines) and `dots_look` (background as a point cloud with a real point count), the speaker kept in colour;
  - `plane_matrix3d` / `homography` (pin captions and titles onto walls, desks, screens), `track_points` (Lucas–Kanade), `track_hands` (MediaPipe Hand Landmarker: palm centre and size per hand), `to_stage`, `setup_three` (offline three.js r181).
- CLI: `heditor matte | depth | look | hands | plane`.
- Six new named styles from a technique study of high-retention tech-creator Reels: `camadas` (concepts drawn behind the speaker), `raio-x` (the machine's view, stage by stage), `duelo` (A/B comparison page), `bancada` (proof on a filmed screen), `manchete` (headline inset on top), `revista` (editorial spreads with the speaker inset).
- New references: `depth-and-3d.md` (toolkit, layer stack, 14 layered recipes, QA) and `technique-catalogue.md` (layouts, illustrations, camera moves, caption systems, hooks, CTAs).
- Setup downloads the person and hand models and three.js; `setup.sh --depth` pre-fetches the depth model (otherwise it downloads on first use). `doctor` checks onnxruntime, `cv2.ximgproc` and the models. Requirements gain `opencv-contrib-python` and `onnxruntime`.
- New `test_depthkit.py` (homography, CSS matrix3d, cover mapping). `plane_matrix3d` writes 12 significant digits (8 decimals left a 0.15 px error on strong perspectives).
- troubleshooting.md: layered-shot pitfalls (double edges, semi-transparent hands, accessories kept by the matte, pumping depth, dense point clouds, offline three.js, render time).

## 1.4.0 — 2026-10-15
- Three new authority styles (serious tone, the speaker as the expert; organic Reels with a comment question and Follow), each with the full recipe:
  - `arquivo-cofre`: archive reading table at night; the expert as a record in a passe-partout, steel drawer with hanging tabs, time-stamp clock, microfilm reel that rewinds to the good day, captions printed on continuous copier paper (white on cobalt);
  - `aduana-de-dados`: night border checkpoint between your computer and the internet; exit declaration, X-ray monitor, barrier, regulations underlined item by item, booth-intercom captions (white on stamp red);
  - `laudo-de-sinistro`: insurance claim forensic report; the expert in the technical photograph with a forensic scale, forensic flash + B&W on every record, coverage clause filled as it is said, pen marks TOTAL LOSS → RECOVERABLE, one-line transcript captions (black on evidence yellow).
- troubleshooting.md: Reels over 70 s fail `heditor test`, music dips with `silence` sections, numeric layout values among timeline keys, `rk.finder` landing on a later occurrence, strips over a low face, tiny text in decorative SVG, camera black in the CTA, empty caption during a stretched word, one-line captions that overflow, repeated tracks inside a batch.
- Idea bank: archive, border checkpoint and forensic case-file formats are now named styles.
- Fix: `prepare_camera` and `styled_camera` rebuild `camera-hd.mp4` and every `camera-<name>.mp4` when they are older than their source. Before, a variant made from a previous `camera-src.mp4` was reused after the EDL changed, so picture and voice drifted apart (seconds) from the first removed sentence on.
- New `scripts/reelkit/camera_sync_check.py <work>`: compares every camera variant with `camera-src.mp4` frame by frame and fails when any is offset or has a different frame count. Run it before rendering whenever the EDL changed.

## 1.3.0 — 2026-10-15
- Fourteen new named styles, each with a full recipe (layout in px, palette, typography, caption contrast, scene grammar, motion, SFX map, music sections, CTA, pitfalls, variations):
  - organic: `tribunal` (courtroom sketch);
  - paid-ad formats with a "Learn more" CTA: `keynote`, `stories`, `predio-24h`, `bilheteria`, `porta-de-aco`, `manual-de-montagem`, `carrinho`, `entrega`, `auditorio`, `album`;
  - authority formats (serious tone, the speaker as the expert): `cassino-de-precisao`, `mesa-de-risco`, `turno-da-madrugada`.
- captions-and-layout.md: presenter cutout (alpha-matted speaker) guidance and the paid-ad safe area (captions at y 1046–1150, nothing critical below 1152, "Learn more" end card).
- quality-gates.md: the CTA test fails by design on "Learn more" ads; document it.
- troubleshooting.md: undefined timeline keys, SVG markers drawn early, gradients on zero-height paths, stale `words-reviewed.json`, upper-cased CTA text, background p95 stuck at −12 dB, DOM overflow checks, numeric HTML entities, colloquial captions in `asr-check`.
- licenses.md: optional external tools used by some styles (matting models, extra OFL font families).
- Idea bank updated: courtroom, stock ticker, checkout and blueprint formats are now named styles.

## 1.2.0 — 2026-10-13
- No dead air: `prepare_cut` now trims the silence at the edges of every block (`lead=0.08`, `tail=0.12` s around the first/last voiced window) and shortens internal pauses longer than 0.35 s (`edge=0.12`). Block boundaries snap to the quietest point of their radius, so junctions used to keep silence from both sides (0.8–1.3 s gaps that read as uncut pauses). `lead=None`/`tail=None` restore the old behaviour.
- New `heditor gaps <work> [max_s]`: lists every silence left in the assembled voice (junction or internal, with surrounding words) and fails above 0.45 s. `heditor test` gained `test_no_dead_air`; the gate is in quality-gates.md and workflow.md.

## 1.1.0 — 2026-10-13
- New named style `missao`: open-world game homage (sunset neon world, in-world social clip, character intro freeze-frame, mission card, GPS route, stats screen, mission-complete banner, phone-chat CTA), born from "creative mode + GTA 6 reference".
- Rendering heavy compositions: documented `PRODUCER_ENABLE_CHUNKED_ENCODE=true` and a larger `FFMPEG_ENCODE_TIMEOUT_MS`.

## 1.0.1 — 2026-10-13
- macOS: `install.sh` no longer uses associative arrays (`declare -A`), which the stock bash 3.2 does not support.
- macOS: `install.sh` and `setup.sh` expand optional argument arrays safely under `set -u` (bash 3.2 treated an empty array as unbound).
- `heditor preview` accepts a relative work directory (the path is resolved before building the file URI).

## 1.0.0 — 2026-10-13
- First public release.
- Ten named styles: cinema, ruptura, impacto, game, thriller, ide, aeroporto, chat, documentario, podcast.
- Creative mode and creative mode with a reference direction.
- reelkit: frame-accurate cuts with measured silence threshold, word-timed ASR, captions (text/pill), HyperFrames page skeleton, face tracking with jump-cut zoom, voice-first multiband mix, two-pass loudnorm, AAC true-peak guard, freeze/top-margin checks, integrity tests.
- One-command setup (tools, venv, Chrome, fonts, music and SFX catalog), `heditor` CLI and multi-agent installer.
