# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Active caption word hard to read | dark text with dark outline on a mid-tone pill | `pill` mode (black on #ffd84d, outline = pill colour) or white on saturated dark; check enlarged crops |
| Accents of titles inside the top margin | Anton glyph ascenders exceed the line box | start titles at ≥ 300 px; confirm with the pixel check |
| Video looks like the previous ones | same skeleton (camera card + boxed panels + pill + PiP finale) reused | creative mode: pick a different world; change camera role, captions system, palette, transitions, CTA |
| Music or SFX cover the voice | short-release ducking, loud impacts on words | keep the kit's held ducking; move impacts into gaps; lower SFX on words to ≤ -20 dB |
| True peak > 0 dBTP in the MP4 although WAV was -2 dB | AAC overshoot from bright transients (beeps, clicks, shutters) | finalize re-limits automatically (`tp_guard`); avoid stacking many bright SFX |
| Freeze detector fails the video | small camera in a UI, intentional holds, planned blackouts | inspect frames; advisory unless the picture is really stuck |
| Pixel top-margin check fails on transitions | full-width stripe/flash wipes | inspect frames; add a dark top band if a world background is bright |
| `≠` or other glyph renders wrong | font lacks the glyph | use a Lucide icon (e.g. `equal-not`) or another font |
| Numbers test fails | unspoken digits on screen (dates, labels, "CAM 01", line numbers) | draw decorative digits with CSS `content`/counters, use words or roman numerals, or list them in `plan["allowed_numbers"]` if truly neutral |
| Caption hidden but still visible | GSAP sets `visibility` on the inner element | hide the outer caption wrapper with `#cap-N{opacity:0 !important}` |
| Preview shows blank video | camera file not ready or wrong `data-start` | wait for `readyState>=2` (preview does), check `data-media-start`/durations |
| Render very slow or killed | low CPU/RAM, many workers | `heditor render <work> 1`; render cuts one at a time; close other heavy jobs |
| ASR misses words at block edges | cut inside a word | widen the block radius in prepare.py, prepare again, re-run `heditor words` |
| Whisper too slow | large model on CPU | `HEDITOR_ASR_MODEL=small`, transcribe windows instead of the full file |
| mediapipe fails to install | Python version without wheels | use Python 3.10–3.13 (setup picks one) |
| `npx hyperframes` asks to install or cannot find Chrome | first run | `npx --yes hyperframes@0.8.147 browser ensure` |
