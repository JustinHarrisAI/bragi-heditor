# Look: bragi on heditor ("quiet operator" editorial, full motion)

The only look Bragi uses for Justin Harris's talking reels. heditor supplies the engine (reelkit, depthkit, GSAP
plugins, count-ups, DrawSVG, MotionPath, SplitText, camera box, SFX catalogue, quality gates); this file supplies the
brand. Read `rules/bragi/RULES.md` first: where heditor's docs, a style file or this file disagree with RULES.md,
RULES.md wins. Read `rules/bragi/learned-notes.md` too: those are Justin's own reject reasons and they bind.

Work in **creative mode** (`skills/heditor/references/creative-mode.md`): invent the edit for this speech, but the
world is always the same family: **an editorial operator's desk in flat Ink**. Think a premium business magazine
spread or a calm operator's console, never neon, never a game, never a blueprint in blue.

The bar (judge rounds 1 and 2): reference reels from Chase AI, Nate Herk and Jack Roberts score motion 8.5 to 9 and
pacing 9. A clean talking head with tasteful captions scores motion 5 to 6.5 and fails. Something meaningful must
change on screen every 1.5 to 2 s, and every change must come from a spoken word.

## World and camera
- Canvas 1080x1920, 30 fps. Ground is flat Ink `#161B1C`. Optional hairline grid in white at 6% (1 px lines,
  60 px pitch) on the Ink ground only, never over footage.
- The camera is a character. Alternate between:
  1. **Full frame** (the plate fills the canvas) for emotional lines and the hook, with real zoom changes on every
     jump cut (1.0, 1.12, 1.0, 1.25; never the same zoom twice in a row) and a slow 3% drift between cuts.
  2. **Spread**: the camera shrinks into a large framed window (about 900 x 1000 px, 8 px corners, no border, no
     shadow) in the upper half while the Ink spread below builds the graphic for the beat (list, numbers, versus,
     timeline). Animate the shrink and return (0.45 s, expo.inOut). Corner ticks in white 70% are allowed.
  3. **Full-screen beat**: 0.7 to 1.2 s with no camera at all, giant Piazzolla type on Ink on the line that carries
     the argument. Audio continues. At most 3 per 30 s, never two in a row.
- Behind-the-head words (depthkit matte) are welcome when the matte is clean on this source; check the matte sheet.
  The source may be a handheld walking selfie: if the matte flickers, skip behind-layer effects.
- Natural colour on the plate. No grade, no `styled_camera` looks (no CCTV, VHS, mono, posterize), no fog, no
  vignette, no bloom. A small exposure or white-balance fix only if the clip needs it.

## Type (only fonts from `looks/bragi/fonts/`, load `fonts.css`)
- **Big words:** Piazzolla Regular 400, 150 to 320 px, line height 1.0, tracking -0.03em, white. The key word of
  the line: Piazzolla Italic 600 in Glow `#A6F0DA`. SplitText per word or per character on the spoken frames.
- **Kickers, labels, units, counters:** Geist Mono 400, uppercase, letter-spacing 0.14em, white 70%, 24 to 34 px.
- **Card body text:** Geist SemiBold 600, white, 40 to 48 px, sentence case.
- Never Anton, Bebas, JetBrains Mono, Inter or any kit font outside `looks/bragi/fonts/`.

## Captions: preset E "Quiet Operator", every spoken word
Geist SemiBold 600, 58 px, sentence case, white, 2 to 4 word chunks grouped by meaning. Flat Ink `#161B1C` band at
78% opacity behind each chunk: 24 px top and bottom, 39 px left and right, 13 px corners, hugs the text, centred,
band top near y 1306 (move between 1150 and 1400 only to stay off the face and inside the safe zone). Unsaid words
62% white, said words 100% with a 1.08 to 1 pop over 0.12 s. Chunk entrance: band 0.96 to 1 plus fade, 0.12 s.
No stroke, no shadow. Hide captions while a full-screen beat shows the same words.

## Colour discipline
Ink `#161B1C`, white, white 70%, Glow `#A6F0DA`. Nothing else: replace every coral, cyan, violet, orange, yellow or
blue from heditor's styles with white, white 70% or Glow. **One Glow element per frame**: a Glow key word, a Glow
stroke, a Glow tick or a Glow counter is each one; if a big word holds Glow, the caption and cards carry none.
No gradients, shadows, text shadows, strokes, outlines, glows or blur halos at rest.

## Motion vocabulary (use heditor's tools, brand-coloured)
- Lines and diagrams draw on with DrawSVG in white (or Glow as the frame's one Glow element).
- Numbers count with integer snap and land on the spoken word ("15 to 20 years" counts).
- Lists build one row per spoken item; a single Glow tick travels from row to row (MotionPath or a y tween).
- Versus or before/after splits slide apart on the turn of the argument.
- Exits move: 0.18 s rise plus fade or a downward slide; never a bare opacity cut.
- Hard cuts only between plates; no crossfades, no glitch, no whip-pan blur trails.
- Hook: frame 1 already moves (punch-in to at least 1.15x) and already carries a big Piazzolla headline of 2 to 5
  words stating the claim, key word in Glow, placed over hat, sky or wall, never across eyes, nose or mouth.

## Sound
heditor's SFX catalogue at its quiet gains (whoosh on camera moves and full-screen beats, click or tick on list
rows, soft data beeps on count-ups, a low impact on the payoff). Voice always on top; -14 LUFS, true peak -1.5 dB.
Music is optional: one calm track from heditor's licensed catalogue, ducked at least 18 dB under the voice.

## End
Last spoken line lands on the biggest moment (a full-screen Piazzolla line). Then a 0.8 s flat Ink end card: white
lockup `looks/bragi/logo/jh-lockup-white.svg` 360 px wide centred, Geist Mono `JUSTINHARRIS.AI` 26 px white 70%
below. No Glow on the end card. No follow-button CTA, no "@yourhandle", no comment-to-DM.

## Words on screen
Only what Justin said, fixed for Whisper mishearings ("AI", "SEO", "Claude"). No invented numbers, no other
creator's handle, no em or en dashes, no hype words.

## QA (in addition to heditor's quality gates)
Contact sheet of 16 moments: at most one Glow element per frame, nothing on the face from eyes to chin, captions on
every spoken word, no colour outside the palette (grep the composition for `#`-colours and `rgb(`), no font outside
`looks/bragi/fonts/`, no em or en dash in any on-screen string, no placeholder text.
