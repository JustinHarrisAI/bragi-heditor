# Captions, layout and camera

## Safe zones (1080×1920)
- Top 0–270 px (14 %): no text, face, logo or key graphic (platform UI). Anton/condensed titles with accents rise above their line box: start titles at ≥ 300 px and verify with the pixel check (first row with luma > 150 on > 8 px must be ≥ 270).
- Bottom ~350 px (y > 1570): only atmosphere; the platform caption/buttons live there.
- Right edge ~120 px between y 1000–1700: like/comment/share buttons; no critical info.
- Face never covered by graphics or captions. Track it (`rk.track_faces`) and place graphics on the opposite side.

## Captions
- Every spoken word, in order, synced (word or phrase level). `plan["captions"]` must match exactly what appears; tests compare it with `words-reviewed.json`.
- Corrections of spelling/brand names live in `words-reviewed.json` (timings untouched). Profanity masked on screen only.
- Size on a phone: ≥ 60 px cap height for phrase captions (Anton 84–96 px), ≥ 46 px for interface-style captions (chat, code, radio).
- Active-word contrast (mandatory): black text on light yellow `#ffd84d` or white, or white text on a saturated dark colour. Never dark text on a mid-tone pill, and never a dark outline around dark letters. In the kit's `pill` mode the outline takes the pill colour.
- Group 1–3 words (≤ 17 chars) for kinetic captions; full phrases for subtitle-like systems; never more than 2 lines.
- World-native caption systems that worked: RPG dialog box with ▼ cursor, code comments typed in an editor, radio transmission in a mono font with amber active word, chat bubbles that grow word by word, documentary subtitles in serif with underlined active word, giant karaoke with one word at a time, film subtitles in lowercase with a blinking keyword.

## Camera treatments
The source webcam is often small (e.g. 320×238 px in meeting recordings). Upscale to ~960 px wide (Lanczos + light unsharp) and never stretch it full height. Ideas: card, circle bubble, monitor/CRT inside a scene, game character window, CCTV feed, video-call window, tilted editorial rectangle with hard shadow, letterbox strip, split screen (two grades of the same feed), clones grid (copies with different grades), PiP that shrinks for a typographic finale, freeze-frame. Pause cuts become shot changes with the jump-cut zoom (1.0 ↔ 1.075 around the face); add a 1–2 % breathing zoom elsewhere.

## Layout patterns
- Hero: camera large between y≈500 and 1200, captions band below (y 1222–1472), headline above (≥ 300).
- Top camera: camera small at the top (y≈280) and graphics in the centre (y 670–1200).
- World UI: the whole canvas is an interface (editor, chat, radar, game) and the camera is one element of it.
- Finale: camera PiP at the top, giant type in the centre for the key line.
