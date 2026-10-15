# Changelog

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
