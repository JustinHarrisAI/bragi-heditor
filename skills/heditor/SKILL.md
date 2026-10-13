---
name: heditor
description: Use when the user wants to edit a talking-head, class, live or podcast video into a vertical Reel/Short/TikTok (1080x1920) with motion graphics, captions, sound design and music — in a named style (cinema, ruptura, impacto, game, thriller, ide, aeroporto, chat, documentario, podcast, missao), in "creative mode" (maximum originality, built for that specific video) or "creative mode + reference" (e.g. "in the style of GTA 6"). Covers setup of all tools, cut selection from transcripts, HyperFrames compositions, voice-first mixing, render and QA.
license: MIT
metadata:
  author: PycodeBR (Felipe Azambuja)
  version: 1.1.0
  homepage: https://github.com/pycodebr/heditor
---

# heditor — creative vertical video editing

heditor turns a recording of someone speaking into a short vertical video that holds attention second by second: a strong opening, a visual world built for what is being said, captions synced word by word, sound effects tied to every action, music with an emotional arc and a call to action. Compositions are HTML + GSAP rendered to MP4 by [HyperFrames](https://github.com/heygen-com/hyperframes). Everything runs locally.

The standard is high: **every video gets an edit designed for it.** A style is a proven visual language, never a template to stamp. If two videos in the same batch look like the same mould, the work is not done.

## 0. Setup (once per machine)

```bash
bash <skill_dir>/scripts/setup.sh          # installs ffmpeg/node/python deps if missing, venv, Chrome, fonts, music, SFX, models
. ~/.heditor/env.sh && heditor doctor       # must end with "heditor is ready."
```

- Re-running setup is safe. `--no-audio` skips the Mixkit library; `--whisper small,medium` pre-downloads ASR models.
- Edit `~/.heditor/brand.json` (name, `@handle`, colours, logo path, Follow/Following words, language). Ask the user for these the first time; never invent a handle.
- If a tool cannot be installed automatically (no sudo/package manager), tell the user the exact command to run and stop.
- All commands below assume `. ~/.heditor/env.sh` was sourced. The CLI is `heditor` (also at `<skill_dir>/scripts/heditor`).

## 1. Choose the mode

| User says | Mode | Read |
|---|---|---|
| "edit in style X", "igual ao estilo X" | Fixed style | `references/styles/<slug>.md` |
| "creative mode", "modo criativo", "surprise me" | Creative mode | `references/creative-mode.md` |
| "creative mode with/using X" (GTA 6, Wes Anderson, anime, news broadcast…) | Creative mode + reference | `references/creative-mode.md` (§ Reference direction) |
| Nothing specified | Ask once which mode; if the user wants you to decide, use creative mode | |

Named styles (`heditor styles`): see `references/styles/INDEX.md` for when each fits.

| Style | Identity |
|---|---|
| `cinema` | One visual metaphor per speech beat, world changes on each turn, live camera card, kinetic captions |
| `ruptura` | Cold open with the strongest line, the camera itself becomes the metaphor, typographic finale |
| `impacto` | Organised layout with coordinated emphasis bursts (type, sound, zoom) on the key lines |
| `game` | The screen is a retro RPG: HUD, dialog-box captions, skills unlocked, inventory, CONTINUE? CTA |
| `thriller` | Security-camera disaster tape: REC overlay, heartbeat, liquid distortion, blackout, system reboot |
| `ide` | Code-editor screencast: circular webcam bubble, captions typed as code comments, terminal CTA |
| `aeroporto` | Control tower: radar, split-flap departures board, flight strips, radio-transmission captions |
| `chat` | Light messaging app: the speaker's sentences arrive as messages, the bot replies, video-call PiP |
| `documentario` | Mini-documentary: letterbox, film grain, serif chapter cards, documentary subtitles, rolling credits |
| `podcast` | Talk show / podcast: saturated set, ON AIR sign, voice-reactive waveform, giant karaoke captions |
| `missao` | Open-world game homage: sunset neon world, in-world social clip, character intro freeze-frame, mission card, GPS route, stats screen, mission-complete banner, phone-chat CTA |

## 2. Workflow (all modes)

Follow `references/workflow.md` step by step. Summary:

1. **Probe the source.** `heditor probe <video> 5 60 300` and look at the frames: where is the speaker (full frame, webcam tile in a meeting, screen share)? Note resolution, the speaker crop, what else is on screen.
2. **Transcribe and choose the cut.** `heditor transcribe <video> 0 <duration> qa/asr-full.json` (or a window). Pick a self-contained argument of 30–70 s: hook → thesis → explanation → conclusion. The hook must exist in the speech. Never invent, reorder words inside a sentence, speed up or splice half-sentences into a new claim. Remove repetitions, false starts and tangents only at clean word boundaries.
3. **Scaffold and prepare.** `heditor new <work> <video>`, fill `BLOCKS`/`CROP` in `<work>/prepare.py`, `heditor prepare <work>`, then `heditor words <work>` and fix spelling/brand names in `words-reviewed.json` (timings untouched; profanity can be masked on screen only).
4. **Design first.** Fill `<work>/DESIGN.md`: video analysis, mode/style, frame map, palette, captions, beat sheet with timestamps, music, CTA, risks. In creative mode, research before designing.
5. **Build.** Rewrite `<work>/build.py` (the template is only a runnable baseline) to implement DESIGN.md. Use the kit (`references/kit-api.md`) or write your own HTML when the format needs it.
6. **Produce.** `heditor produce <work> music:<id> <drop_s>` → composition + voice-first mix; read the `balance` it prints.
7. **QA before render.** `heditor lint <work>` (0 errors) → `heditor preview <work> <18–24 times>` → inspect the contact sheet with vision and fix every defect → `heditor test <work>`. Gates in `references/quality-gates.md`.
8. **Render and finalize.** `heditor render <work>` → `heditor finalize <work> <name>.mp4` → review `qa/final-contact-sheet.jpg` and `qa/final-verification.json` → `heditor asr-check <work>`.
9. **Deliver** the MP4 path with a short summary (format, music, what was verified, what nobody has checked: nobody has *listened* to it — say so). Never publish to social networks unless the user explicitly asks.
10. **Learn.** If you created a new style that the user liked, add it as a named style (`references/adding-styles.md`).

## 3. Non-negotiables

- **Voice first.** Music ≈ 21.5 dB under the voice (median), background ≥ 12 dB under at p95, impacts in the gaps, ducking held across the whole phrase. -14 LUFS, true peak ≤ -1.5 dBTP after AAC.
- **Readable captions.** Every spoken word, synced; active word with high contrast (black on light yellow, white on saturated dark — never dark-on-mid or dark outline on dark text). Check enlarged crops.
- **Safe zones.** Nothing important above y = 270 (top 14%; titles with accents start ≥ 300), keep the bottom ~350 px and the right edge (~120 px, y 1000–1700) free of critical info, never cover the face.
- **Truth.** Numbers, names and claims exactly as spoken; no invented stats, testimonials, promises or private data; no third-party logos or copyrighted assets (homage through type, colour, motion, sound).
- **Licences.** Fonts OFL (google/fonts), icons Lucide, music/SFX from the catalog (Mixkit Free License) or user-provided licensed files. Record provenance in DESIGN.md.
- **Different every time.** In a batch, give each video its own format (layout, camera treatment, captions, palette, transitions, music, CTA). Ask vision to compare contact sheets: "do these look like the same template?" If yes, change more.
- **Verify before claiming.** A video is done only after lint, previews, tests, render, finalize gates and contact-sheet review pass. Report what failed honestly.

## 4. References

- `references/workflow.md` — the full procedure with commands, cut selection and EDL rules.
- `references/creative-mode.md` — creative mode, reference-directed creative mode, research method, idea bank.
- `references/kit-api.md` — reelkit functions, page skeleton, GSAP helpers, plan/sound/music formats.
- `references/sound-design.md` — voice chain, mix targets, SFX vocabulary, music catalog and section design.
- `references/captions-and-layout.md` — caption systems, contrast rules, safe zones, camera treatments.
- `references/quality-gates.md` — every gate, how to read false positives, final checklist.
- `references/adding-styles.md` — how to turn a successful edit into a new named style.
- `references/troubleshooting.md` — known failures and fixes.
- `references/licenses.md` — third-party components and asset licences.
- `references/styles/` — one file per named style.
