# Quality gates

A cut is delivered only when all required gates pass (or a flagged item was inspected and documented as intentional).

| Gate | Command / file | Pass |
|---|---|---|
| Speech integrity | `words-reviewed.json`, `edl.json` | only spoken words, 1× speed, no clipped words at block edges (check ASR at each junction) |
| Dead air | `heditor gaps <work>` | no silence > 0.45 s inside the speech (junctions included); run right after prepare |
| Design | `DESIGN.md` | analysis, mode/style, beat sheet, music, CTA, risks written before building |
| Lint | `heditor lint <work>` | 0 errors (caption-structure warnings are normal) |
| Mix balance | `qa/balance.json` | music ≤ -21 dB vs voice (median), background p95 ≤ -12 dB, < 5 % windows within 10 dB |
| Previews | `heditor preview` + vision | no overlaps, clipped text, face coverage, low-contrast active word, placeholder look, text above 270 px |
| Distinctness (batches) | vision on contact sheets | videos do not look like the same template |
| Tests | `heditor test <work>` | all pass (captions = words, no overlap, CTA with handle + Follow/Following, events in timeline, balance, no unspoken numbers, no "illustrative"/placeholder tags, no dead air) |
| Render | `heditor render` | exit 0 |
| Final file | `qa/final-verification.json` | no decode errors, -15 ≤ LUFS ≤ -13, true peak ≤ -1.5 dBTP, audio/master correlation ≥ 0.99, top margin ≥ 270 |
| Final frames | `qa/final-contact-sheet.jpg` + vision | no defects |
| Masking | `heditor asr-check <work>` | master similarity ≥ 0.90 and ≥ (clean voice − 0.03) |

## Reading flags
- **Freezes** (`freezedetect`, 0.3 s) are advisory. They fire on intentional holds (CTA built in steps, final card), planned blackouts and when the camera is small inside a UI and the speaker is still. Extract the flagged frames and confirm with vision; fail only if the picture is really stuck (a video that did not load, a broken scene).
- **Top margin** by pixels also fires on full-width decorative transitions (stripe wipes, flashes). Check the flagged frames; real text/graphics above 270 px must be fixed.
- **True peak** after AAC: finalize re-limits automatically and records `tp_guard`; LUFS can end ~0.8 dB lower — acceptable.

## Final checklist for the delivery message
Format/style and why; duration; music (title, artist, licence); what was verified (gates above); flagged items and decisions; what was not verified (nobody listened; colour on other screens); file path/link. Never publish without explicit permission.
