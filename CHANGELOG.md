# Changelog

## 2.1.1 — 2026-10-18
- `track_faces` detects on a copy downscaled to at most 640 px wide (positions are fractions, so results are unchanged). Decoding 5 fps of full-HD RGB frames for a 78 s cut used ~2.4 GB and was killed by the OOM killer on a 8 GB VPS.
- Troubleshooting: 4K HEVC phone recordings (e.g. iPhone `.MOV`) can also exhaust memory in `heditor prepare`; make a 1080×1920 proxy and use it as `SOURCE`.
- Validated on a 78 s first-person phone recording in the `nativo` style (`full` mode, no face in frame).

## 2.1.0 — 2026-10-16
- **New style `nativo`** (family *native*): a clean native edit with only cuts at clean word boundaries, jump cuts that alternate the framing (1.0/1.075 on the face of each segment) and animated word-by-word captions (Inter 900, black on a light-yellow pill). No music, SFX, graphics or end card unless asked. Ships a reference build in `templates/styles/nativo/build.py` with two camera modes: `full` (vertical source, or a 9:16 crop around the median face from the full-resolution source, frame for frame) and `fit` (camera fitted to the width over a blurred copy of itself, for small or wide sources).
- `heditor new <work> <video> --style <slug>` seeds `build.py`/`DESIGN.md` from `templates/styles/<slug>/` when the style has a reference build.
- `heditor produce <work> none 0` builds without a music track (the mix stays voice only).
- `heditor test`: a Reel may end with the speech, without a CTA screen, when the plan declares `"end_card": false`.
- Long-form style pack `nativo`; style packs may set an SFX category to `None` to stay silent.
- `camera_sync_check` checks blurred background variants (`*blur*`) by frame count only, instead of reporting noise as a sync failure.
- Validated on a 35 s cut in `fit` mode (lint 0 errors, `heditor test` 10/10, render about 4 min, −14.1 LUFS, final camera within one frame of the source); `full` mode exercised on the same cut (frame-exact 9:16 crop).

## 2.0.0 — 2026-10-16
- Quality gate and troubleshooting row for short labels that stay on screen (overlapping fade-in/fade-out tweens), found in the narrated documentary production.

Long-form and multi-format editing, style packs for every named style, Reels up to 180 s and a new narrated-documentary style. Existing 9:16 projects build and render as before.

### Long-form mode
- **Long-form mode** (classes, lives, YouTube videos; minutes to hours) — `heditor new --long` and `heditor long transcribe | edl | apply | chapters | layouts | produce | preview | render | finalize | qa | subs | sync | estimate | styles`, documented in `references/long-form.md`:
  - chunked, resumable ASR with boundaries in silences and a progress/ETA log;
  - reviewable EDL proposal (`edl-proposal.json` + `qa/edl-proposal.md`): dead pauses shortened by energy (never by ASR timing), immediate repetitions, false starts and per-language fillers removed at the quietest point of word gaps, low-confidence cuts left for review, manual `exclude` ranges with their surrounding silence trimmed; `apply` assembles screen, camera and voice in single passes on the source frame grid (frame counts checked) and remaps the words without a second ASR (spelling fixes carried by source time; `--words-only`);
  - layouts for screen share + camera (`pip`, `screen` with zoom, `speaker`, `side`) switched per passage, with suggestions from screen activity; chapters (suggestion, YouTube rules, cards, current-chapter tag, description timestamps); burned captions fitted with the real fonts and SRT/VTT export; lower thirds; intro card; closing CTA `follow` (Follow → Following) or `youtube` (Subscribe → Subscribed + "Watch next" slots);
  - style packs (`stylepacks.py`) for all 36 named styles (palette, typography, captions with tested active-word contrast, frame, overlays, transition, chapter card, lower third, camera grade, SFX, music) with vertical → horizontal adaptation rules; creative set pieces (`title`, `concept_map`, `checklist`, `callout`, `custom`) and an automatic retention plan at the cadence of each kind (aula, live, youtube);
  - segmented, resumable render: one HyperFrames composition per segment (chapter-aware, ≤ 60 s, frame-exact) that plays the global timeline from its start, skipped when unchanged, render log with seconds per frame and ETA, optional per-segment heavy-job lock (`HEDITOR_LOCK`); concat without re-encoding and one continuous master audio muxed at the end;
  - memory-bounded voice-first mixer for long timelines (`longmix.py`, same balance targets, loudness from `long.json`);
  - long-form QA report (`longqa.py`): duration/canvas, decode, loudness (−14 LUFS default), audio/master correlation, camera/screen/voice sync against the source, sampled-window ASR, chapters, segment seams (black or duplicated frames), contact sheets ≤ 1400 px.
- `heditor test` understands long-form plans (`mode: "long"`): CTA by `cta.kind`, intro offset, optional captions, pauses up to 0.6 s, no 180 s cap.
- `camera_sync_check.py --source` (also `heditor long sync`): camera, screen and voice compared with the original recording through the EDL; module docstring and messages in English.
- `rk.load_brand` fills `subscribe`, `subscribed` and `watch_next` from the brand language when absent.

### Format profiles and style packs
- **Format profiles** (`scripts/reelkit/formats.py`, `heditor formats`): 9:16 (unchanged Reel numbers), 16:9, 16:9 4K, 1:1, 4:5 with canvas, safe area, caption zone, lower third and camera layouts. Used by `preview` (viewport from the composition), `finalize` (safe top row and sheet aspect per profile), `prepare_cut` (`crop="fit:<fmt>"`, `format` in `edl.json`), `rk.page(fmt=...)` and `heditor test`. Existing 9:16 projects behave as before.
- **Style packs** for the 36 named styles: `stylepacks.py` (`sp.get`, `sp.css_vars`, `heditor long styles`), the vertical → horizontal adaptation table in `references/long-form.md`, and `adding-styles.md` now asks every new style for its pack (`test_formats.py` fails when a style file has no pack).

### Longer Reels
- `heditor test` accepts longer Reels (narrated documentaries, stories of ~90 s): `plan["max_duration"]` (or `HEDITOR_MAX_DURATION`) raises the default 70 s limit up to 180 s, the Instagram Reels maximum.

### New style: `documentario-narrado` (alias atlas)
- Large-scale narrated documentary: the speaker's voice is the narration and a living night globe is the spine (Natural Earth, public domain, orthographic canvas with a virtual camera flight, lights that switch on with acceleration and land on the spoken number, great-circle routes fired on each repetition of the verb, world-scale payoff); generated period paintings in one constant style with 2.5D parallax; dated cards with a music-only hard silence → low impact → reveal → amber flash; the narrator as a film-graded testimony plate, a gold medallion on the map or voice-over; documentary notes with verified, sourced facts; a music tree in sections (era radio, filtered, full with the lift on the climax word, synthesized drone, silences, one trailer hit); "next chapter" loop back to the first globe shot. Full recipe, render cost and production pitfalls in `references/styles/documentario-narrado.md`; row in INDEX, SKILL, README, creative-mode, the style pack and the long-form table.
- depthkit: `dk.still_layers(src, out_dir)` splits a still (a generated painting, a photo) into a background and a soft RGBA front layer for 2.5D parallax; `dk.front_alpha` is the tested pure helper.
- troubleshooting.md: generated images in another aspect ratio, pseudo-text in generated paintings, animated `letterSpacing` lint error, vision timeouts on large sheets, music-only dramatic silences, documentary fact notes and the numbers test, canvas worlds that slow the render. quality-gates.md: a gate for unspoken facts on screen; cards listed among expected freeze flags.

### Fixes and tooling
- Long-form set pieces keep the speaker visible: checklists dim only the screen (world-level dim under the camera) and the full-screen concept map uses an opaque background instead of leaving a dark ghost of the camera.
- The `heditor` CLI exports `HEDITOR_KIT`/`HEDITOR_SKILL` pointing at its own checkout, so a second checkout never imports another checkout's kit through `env.sh`.
- New tests: `test_formats.py` (profiles, layouts, style packs) and `test_longform.py` (EDL, chapters, captions, segments, page windows, concatenation, audio/video assembly); CI runs them; `test_depthkit.py` gains a test for `front_alpha`.

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
