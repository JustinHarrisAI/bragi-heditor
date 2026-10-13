# Kit API (scripts/reelkit)

Import in a cut's `build.py`:
```python
import os, sys; from pathlib import Path
sys.path.insert(0, os.environ.get("HEDITOR_KIT", str(Path.home() / ".heditor/kit")))
import reelkit as rk
```

## Brand and assets
- `rk.load_brand(work)` → dict `name, handle, logo, lang, follow, following, comment, colors{bg,bg2,accent,accent2,alert,ok}` (work/brand.json overrides ~/.heditor/brand.json).
- `rk.setup_assets(work)` copies fonts (all from `~/.heditor/assets/fonts`), `gsap.min.js`, `grain.png`, Lucide licence and the brand logo as `assets/logo.png` into `<work>/composition/assets`.
- Fonts available after setup (file names to use in `@font-face`): `Anton-Regular.ttf`, `VT323-Regular.ttf`, `Geist-VF.ttf`, `Inter-VF.ttf`, `JetBrainsMono-VF.ttf`, `IBMPlexMono-Regular.ttf`, `IBMPlexMono-Bold.ttf`, `PressStart2P-Regular.ttf`, `PlayfairDisplay-VF.ttf`, `PlayfairDisplay-Italic-VF.ttf`, `Fraunces-VF.ttf`, `BebasNeue-Regular.ttf`, `DMSerifDisplay-Regular.ttf`, `Caveat-VF.ttf`, `B612Mono-Regular.ttf`, `B612Mono-Bold.ttf`, `Fredoka-VF.ttf`. Need another? Download it from google/fonts (OFL) into `composition/assets` with its licence.
- `rk.ensure_icons(["name", ...])` downloads Lucide SVGs; `rk.icon(name, cls="ic")` returns inline SVG.
- `rk.prepare_camera(work, width=960)` → upscaled, lightly sharpened `camera-hd.mp4` (returns width, height).
- `rk.styled_camera(work, name, vf)` → `camera-<name>.mp4` from camera-hd with an ffmpeg filter chain. Examples: CCTV `eq=saturation=0.25:contrast=1.2,colorbalance=gs=.08,noise=alls=18:allf=t` · pixel `scale=160:-2:flags=neighbor,scale=960:-2:flags=neighbor` · warm film `curves=preset=increase_contrast,colortemperature=temperature=4800,noise=alls=6:allf=t` · radar green `format=gray,format=rgb24,colorchannelmixer=.2:.2:.2:0:.7:.7:.7:0:.25:.25:.25:0`.
- `rk.prepare_voice(work)` → `voice-master.wav` (declip, high-pass, adaptive denoise, -2.5 dB @250 Hz, +2.5 dB @3.2 kHz, de-esser, 3:1 compressor, limiter).

## Words and captions
- `rk.load_words(path, censor=None)` → `[{word, shown, start, end}]` sorted.
- `rk.finder(words)` → `f(token, after=0.0)` returns the start of the first matching word (case/punctuation-insensitive) after a time. Use it for key moments.
- `rk.captions(words, voice_end, max_words=3, max_chars=17)` → groups `{id, start, end, text, words}`; never overlapping.
- `rk.captions_html(caps)` / `rk.captions_js(caps, mode="text"|"pill")` → default caption band (Anton, uppercase, y 1222–1472). Write your own renderer for world-native captions but keep `plan["captions"]` identical to what appears.

## Page skeleton (optional)
`rk.page(title, duration, card_w, card_h, face_origin, videos, scenes_html, css, js, keys, caps, world_back="", overlays="", caption_mode="text", brand_work=work)` builds a HyperFrames page with:
`#stage > #world > #bg, world_back, #glow-a/#glow-b, .floor, #horizon, .speed, #rig-aura, #rig > #squeeze > #frame > #cam-zoom > #cam-breath > #cam-jump > videos, #cam-tint, #cam-scan, #cam-over, #border; scenes_html; overlays; #vignette; .conf` + caption band + `#grain`, `#flash` + `audio#master`. CSS variables `--bg --bg2 --accent --accent2 --alert --ok` come from the brand.
- `rk.rig_states(card_w, card_h)` → `{"hero": {...}, "top": {...}}` (add your own states, e.g. `pip`). `keys["rig"] = [[t, state, dur], ...]`.
- `rk.SAFE_TOP = 270`, `rk.CARD_BOTTOM_MAX = 1200`, `rk.PANEL_TOP_MIN = 670`.
- Writing your own page is encouraged for creative formats. Requirements: root `<main id="stage" data-composition-id="main" data-start="0" data-duration=".." data-width="1080" data-height="1920" data-fps="30">`; media as `.clip` elements with `data-start`, `data-duration`, `data-track-index` (unique per track); `<audio class="clip" src="assets/master.wav">`; one paused GSAP timeline registered as `window.__timelines.main`; deterministic (seeded random only, no Date/Math.random).

## JS helpers (BASE_JS, available inside `js`)
`S(sel, vars, t)` set · `TO(sel, vars, t)` to · `FT(sel, from, to, t)` fromTo · `out(sel, t, vars)` fade out · `pop(sel, t)` · `shake(t, amp)` on `#world` · `flash(t, peak, dur, color)` · `punch(t, scale, hold, back)` camera zoom · `rig(state, t, dur)` · `confetti(t, x, y)` · `speedlines(t)` · `rnd()` seeded (`keys["seed"]`). `K` = keys, `D` = duration. `K.segments` (from `rk.jump_segments`) drives jump-cut zoom 1.0↔1.075 and 1.5% breathing on `#cam-jump/#cam-breath`.

## Face tracking
`faces = rk.track_faces(work, video="camera-hd.mp4", step=0.2)` (MediaPipe) → `qa/face-track.json`; `rk.jump_segments(work, faces, voice_end)` → segments between EDL cuts with the median face centre (never smoothed across a cut). Use the face centre for zoom origins and to place graphics on the opposite side.

## Plan formats
- Sound event: `{"time": s, "category": "whoosh", "variant": 0, "gain_db": -14, "rate": 1.0, "length": 0.6, "context": "why"}`. Categories: `rk.sfx_library().keys()`.
- Music section: `{"start", "end", "mode": "full|radio|lowpass|muffled|vhs|retro|silence", "gain_db", "track", "src" (seconds inside the track), "fade_in", "fade_out"}`. `rk.music_path("music:955")` → local file.
- `rk.mix(work, plan, rk.sfx_library(), music_body_db=-21.0, music_duck=0.80, sfx_offset_db=-7.0, sfx_duck=0.85, multiband=True, low_duck=0.55)` → writes `master.wav` (two-pass loudnorm -14 LUFS) and `qa/balance.json`; returns the balance. A build may define `sfx_lib()` to extend the library (e.g. synthesized sounds).
