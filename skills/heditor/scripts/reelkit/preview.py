"""Fast frame previews of a composition (deterministic seek in headless Chromium).

Usage: preview.py <sheet.jpg> <t1,t2,...> <work_dir>   -> PNG frames + a contact sheet in <work>/qa.
Env HEDITOR_CHROME: optional browser executable; default is Playwright's Chromium.
"""

import json
import os
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

WORK = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(".")
CHROME = os.environ.get("HEDITOR_CHROME") or None

SEEK = """async (t) => {
  window.__timelines.main.seek(t,false);
  document.querySelectorAll('.clip').forEach(el=>{
    const s=+el.dataset.start||0, d=+el.dataset.duration||1e9;
    el.style.visibility=(t>=s&&t<s+d)?'visible':'hidden';
  });
  await Promise.all(Array.from(document.querySelectorAll('video')).map(v=>new Promise(res=>{
    const s=+v.dataset.start||0, m=+(v.dataset.mediaStart||0);
    const target=Math.max(0,Math.min(m+(t-s),v.duration-.05));
    if(Math.abs(v.currentTime-target)<.01){res();return;}
    v.addEventListener('seeked',res,{once:true});v.currentTime=target;
  })));
}"""


def main(times, out_name):
    qa = WORK / "qa"
    qa.mkdir(exist_ok=True)
    errors = []
    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            **({"executable_path": CHROME} if CHROME else {}),
            headless=True,
            args=["--no-sandbox", "--allow-file-access-from-files", "--autoplay-policy=no-user-gesture-required"],
        )
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda m: errors.append("console:" + m.text) if m.type == "error" else None)
        page.goto((WORK / "composition/index.html").as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_function("Array.from(document.querySelectorAll('video')).every(v=>v.readyState>=2)")
        for t in times:
            page.evaluate(SEEK, t)
            path = qa / f"pv-{t:06.2f}.png"
            page.screenshot(path=str(path))
            shots.append(path)
        browser.close()
    cols = 6
    w, h = 270, 480
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "black")
    for i, path in enumerate(shots):
        im = Image.open(path).convert("RGB").resize((w, h))
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(qa / out_name, quality=88)
    print(json.dumps({"errors": errors, "sheet": str(qa / out_name)}, ensure_ascii=False))


if __name__ == "__main__":
    ts = [float(x) for x in sys.argv[2].split(",")]
    main(ts, sys.argv[1])
