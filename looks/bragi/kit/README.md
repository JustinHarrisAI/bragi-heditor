# Bragi kit: hand-made motion components

Justin designs these by hand in a separate session. Bragi loads them on every run. When a beat in a reel needs a
graphic, Bragi uses a kit component if one fits and builds fresh only when nothing matches. Every fresh build is
written to `wishlist.md` so the next kit session knows what to design.

## Folder layout

```
looks/bragi/kit/
  README.md            this file (the contract)
  wishlist.md          graphics Bragi had to build fresh (Justin's design brief)
  index.json           catalogue Bragi reads first (one entry per component)
  <component-id>/
    component.html     the component: one self-contained HTML fragment (markup + scoped CSS)
    component.js       registers the animation on the composition's GSAP timeline (see "Contract")
    props.json         JSON Schema of the props the component accepts
    preview.mp4        a 1080x1920 render of the component with its example props, 2 to 6 s
    preview.json       the example props used for preview.mp4
    assets/            optional SVG, Lottie JSON, fonts or images the component needs (relative paths only)
```

## index.json entry

```json
{
  "id": "serp-climb",
  "name": "SEO ranking climbs a Google results page",
  "concepts": ["seo", "google", "ranking", "search", "first page"],
  "duration_s": [1.5, 4.0],
  "layout": "full-screen | top-zone | lower-third | behind-speaker",
  "needs_cutout": false,
  "accent": "#A6F0DA",
  "version": "1.0.0"
}
```

`concepts` are the spoken words or ideas that should trigger the component. Bragi matches them against the
transcript of each beat.

## Contract (HyperFrames + GSAP, deterministic)

- `component.html` is a fragment with one root element: `<div class="kit-<id>" data-kit="<id>">...</div>`.
  All CSS is scoped under `.kit-<id>`. No external network requests; fonts and assets load from `assets/`.
- `component.js` exports one function on `window.BragiKit`:

  ```js
  window.BragiKit = window.BragiKit || {};
  window.BragiKit["serp-climb"] = function (root, tl, at, props) {
    // root: the component's root element inside the composition
    // tl:   the composition's single paused GSAP timeline
    // at:   start time in seconds on that timeline
    // props: validated against props.json
    // add every tween to tl at (at + offset); return the component's total duration in seconds
    return 3.2;
  };
  ```

- Seekable and deterministic: everything lives on `tl` (no free-running `requestAnimationFrame`, no `Date.now`,
  no `Math.random` without a seed passed in props). Lottie is driven by `goToAndStop` from the timeline.
- Canvas 1080x1920. Keep text out of the top 220 px and the bottom 380 px (platform UI), and never over the
  speaker's face (eyes to chin). Components with `needs_cutout: true` sit behind the speaker cutout layer.
- Accent colour comes from props (`accent`, default Glow `#A6F0DA`). No em or en dashes in any text.
- Every number, name and claim shown comes from props, never hard-coded, so the accuracy gate can check it
  against the transcript.

## Props

`props.json` is a JSON Schema. Common props: `accent`, `text`, `items` (array), `value_from` / `value_to`
(numbers), `label`, `intensity` (0 to 1: strong is about 0.7, wild is 1.0).

## How Bragi uses the kit

1. Read `index.json`. For each beat, pick a component whose `concepts` match what Justin says.
2. Copy the component folder into the composition, include `component.html`, load `component.js`, and call
   `BragiKit[id](root, tl, at, props)` on the beat's word timestamp.
3. If nothing fits, build the graphic fresh and append it to `wishlist.md` (format below).

## Preview

`preview.mp4` is rendered with HyperFrames from a minimal composition that mounts the component with
`preview.json` props on an Ink `#161B1C` background. It is the thumbnail Justin and Bragi both look at.
