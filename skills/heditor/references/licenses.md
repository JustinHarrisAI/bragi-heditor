# Third-party components and licences

| Component | Use | Licence | How it reaches the user |
|---|---|---|---|
| HyperFrames (`hyperframes@0.8.147`, HeyGen) | HTML → MP4 rendering, lint | Apache-2.0 | `npx` at runtime |
| Chrome headless shell | rendering and previews | Chrome terms | downloaded by `hyperframes browser ensure` |
| GSAP 3.14.2 (GreenSock/Webflow) | animation timeline | GSAP standard "no charge" licence (https://gsap.com/standard-license) | downloaded from jsDelivr by setup |
| faster-whisper + CTranslate2 Whisper models | ASR with word timestamps | MIT (models: MIT) | pip + Hugging Face download |
| MediaPipe + BlazeFace short range | face tracking | Apache-2.0 | pip + Google storage download |
| FFmpeg | cutting, grading, audio, encoding | LGPL/GPL (system build) | system package |
| Playwright (Python) | deterministic frame previews | Apache-2.0 | pip |
| NumPy, Pillow, pytest | processing, images, tests | BSD/MIT-CMU/MIT | pip |
| Fonts from github.com/google/fonts | typography | SIL Open Font License 1.1 | downloaded by setup with OFL.txt files |
| Lucide icons | inline SVG icons | ISC | downloaded on demand |
| Mixkit music and sound effects | soundtrack and SFX | Mixkit Stock Music Free License / Mixkit Sound Effects Free License (https://mixkit.co/license/) | downloaded by setup from Mixkit's CDN to the user's machine; never redistributed in this repository |

Your own videos, logos and any extra music/SFX you add are your responsibility. Do not use third-party logos, trademarks, characters or copyrighted music/footage in homage styles.
