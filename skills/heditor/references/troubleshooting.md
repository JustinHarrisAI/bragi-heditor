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
| Render dies with "FFmpeg killed after exceeding ffmpegEncodeTimeout" | heavy composition (gradients, filters) + loaded machine | re-render with `PRODUCER_ENABLE_CHUNKED_ENCODE=true FFMPEG_ENCODE_TIMEOUT_MS=7200000`; limit blur/backdrop-filter |
| asr-check delta below -0.03 but the voice is clear | the small Whisper model mishears a phrase in both files differently | re-check the flagged window with `HEDITOR_ASR_CHECK_MODEL=medium` (or a windowed medium transcription) before changing the mix |
| Render very slow or killed | low CPU/RAM, many workers | `heditor render <work> 1`; render cuts one at a time; close other heavy jobs |
| ASR misses words at block edges | cut inside a word | widen the block radius in prepare.py, prepare again, re-run `heditor words` |
| Whisper too slow | large model on CPU | `HEDITOR_ASR_MODEL=small`, transcribe windows instead of the full file |
| A tween lands at the very end of the timeline | a key used in the JS (`K.someword`) is undefined, so GSAP gets `NaN`/`undefined` as the position without any error | validate in build.py that every `K.x` referenced by the JS exists before writing the page |
| SVG arrowheads visible before the line is drawn | `marker-end` renders even when `stroke-dashoffset` hides the stroke | keep the path at opacity 0 until its stroke starts drawing |
| A gradient stroke does not paint on a straight line | `linearGradient` with `objectBoundingBox` on a path of zero height | use a solid colour or `gradientUnits="userSpaceOnUse"` |
| Captions keep timings of an older cut | `heditor words` does not overwrite an existing `words-reviewed.json` | after re-running prepare, regenerate `words-reviewed.json` from the new `words.json` and re-apply spelling fixes |
| CTA test fails although Follow is on screen | button text was upper-cased in Python | write the exact `brand.json` words in the HTML and upper-case with CSS `text-transform` |
| Background p95 stuck at exactly −12.0 dB | the mix calibration stops at the threshold when weak-voice windows (pauses, stretched vowels) dominate | add 3–5 dB music dips on those windows with sections that keep `src` continuous |
| Text clipped inside a box but the contact sheet looks fine | reduced sheets hide overflow | check overflow in the DOM (Playwright) and review native frames one by one; very large sheets can time out the vision model |
| Numbers test fails on an arrow | numeric HTML entities (`&#8627;`) count as digits | use the literal character or an icon |
| `asr-check` similarity drops on colloquial captions | the small model normalises spoken contractions to the formal word | expected; compare against the clean voice delta, not the absolute value |
| `heditor test` fails on duration | the Reel is longer than 70 s | plan the speech for ≤ 66 s before cutting (the CTA needs ≥ 4 s); drop context lines, not the hook or the rule |
| Need a music dip without restarting the track | splitting a section restarts `src` and can land on another part of the file | append a section `{"mode":"silence","start":a,"end":b,"gain_db":host_gain-5}` after the section that plays there: `silence` is not decoded, but its `gain_db` (absolute, not relative) replaces the gain of that window |
| `test_key_moments_in_speech_order` fails although every beat is in the speech | numeric layout values (sizes, offsets) were stored in `plan["keys"]` and are read as times | keep only times in `keys`; put layout constants in a nested dict (e.g. `K.cfg`) |
| An animation fires on the wrong word after a re-cut | `rk.finder(token, after=t)` returns the first match after `t`; removing a passage moves the next occurrence earlier | re-validate every key against the transcript after each new prepare; prefer distinctive tokens |
| An impact strip "over the torso" covers the chin | the face sits low in a webcam tile (centre ≈ 70 % of the height) | measure the face (`qa/face-track.json`) before placing strips; put the strip at the top of the camera, over the background |
| Vision calls a decorative object broken text or a stray letter | tiny text (< 16 px) or lone glyphs inside a decorative SVG (scales, rulers) | draw decorative objects without inscriptions |
| The camera window goes black in the CTA | the camera clip ends with the last word | extract the last frame (`ffmpeg -sseof -0.2 … -frames:v 1`) and show it as a still (or freeze it graded) |
| The caption area is empty for a moment | a stretched word or connective leaves a gap between groups | keep the current group on screen until the next one when the gap is < 0.7 s |
| A one-line caption overflows its strip | long words at a fixed size | compute the font size per group with the real fonts (PIL `getlength`, variable axes set) and shrink to fit |
| Two cuts of a batch share the same soundtrack | each agent picked the best-matching track alone | record the music id of every cut in the batch brief and give each cut a different track before producing |
| mediapipe fails to install | Python version without wheels | use Python 3.10–3.13 (setup picks one) |
| `npx hyperframes` asks to install or cannot find Chrome | first run | `npx --yes hyperframes@0.8.147 browser ensure` |

## Picture and voice out of sync after changing the cut

**Symptom:** the first seconds are in sync, then the mouth runs seconds ahead of or behind the voice (often from the first sentence removed in a revision). Captions still match the voice.

**Cause:** the EDL changed (`heditor prepare` rewrote `camera-src.mp4` and the voice) but the derived camera variants (`camera-hd.mp4`, `camera-grade.mp4`, `camera-mono.mp4`…) were built from the previous `camera-src.mp4`. Up to 1.3.0 they were only built when missing. A frame-count mismatch between `camera-src.mp4` and the variants is the giveaway.

**Fix:** since 1.4.0 the kit rebuilds variants older than their source. Check with `python scripts/reelkit/camera_sync_check.py <work>` (every variant must report offset 0 and the same frame count), run `heditor produce` again and re-render. On a project made with an older kit, delete the stale `camera-*.mp4` variants (keep `camera-src.mp4`) or `touch composition/assets/camera-src.mp4` before producing.

