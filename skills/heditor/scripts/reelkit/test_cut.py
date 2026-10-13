"""Integrity tests for any heditor cut. Usage: CUT_WORK=<work_dir> pytest -q test_cut.py"""

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

WORK = Path(os.environ["CUT_WORK"])
sys.path.insert(0, str(Path(__file__).parent))
import reelkit as rk  # noqa: E402
BRAND = rk.load_brand(WORK)
PLAN = json.loads((WORK / "plan.json").read_text())
HTML = (WORK / "composition/index.html").read_text()
_words = WORK / "words-reviewed.json" if (WORK / "words-reviewed.json").exists() else WORK / "words.json"
SOURCE = json.loads(_words.read_text())
SOURCE = SOURCE if isinstance(SOURCE, list) else SOURCE["words"]


def test_caption_tokens_match_source_once():
    out = Counter((w["word"].strip(), round(w["start"], 3)) for c in PLAN["captions"] for w in c["words"])
    src = Counter((w["word"].strip(), round(float(w["start"]), 3)) for w in SOURCE)
    assert out == src


def test_captions_ordered_without_overlap():
    caps = PLAN["captions"]
    for a, b in zip(caps, caps[1:]):
        assert a["start"] < a["end"] <= b["start"] + 1e-6
    assert caps[-1]["end"] <= PLAN["voice_end"] + 1e-6


def test_duration_and_cta():
    assert PLAN["duration"] <= 70
    assert PLAN["duration"] - PLAN["voice_end"] >= 4.0
    assert BRAND["handle"] in HTML, "CTA must show the brand handle"
    assert BRAND["follow"] in HTML and BRAND["following"] in HTML, "CTA must show the Follow -> Following state"


def test_sound_events_inside_timeline():
    for ev in PLAN["sound_events"]:
        assert 0 <= ev["time"] < PLAN["duration"]


def test_key_moments_in_speech_order():
    k = PLAN["keys"]
    times = [v for key, v in k.items() if isinstance(v, (int, float)) and key not in ("voice_end", "duration", "seed", "brk")]
    assert all(0 <= t <= PLAN["voice_end"] for t in times)


def test_no_editorial_tags():
    lower = HTML.lower()
    for tag in ["ilustrativ", "imagem de banco", "illustrative", "stock footage", "placeholder", "lorem ipsum"]:
        assert tag not in lower


def test_voice_first_balance():
    b = json.loads((WORK / "qa/balance.json").read_text())
    assert b["music_minus_voice_median_db"] <= -21.0
    assert b["bed_minus_voice_p95_db"] <= -11.5
    assert b["windows_bed_within_10db_pct"] < 5


def test_numbers_only_from_speech():
    visible = re.sub(r"<head>.*?</head>|<script.*?</script>|<style.*?</style>", "", HTML, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", visible)
    spoken = set(re.findall(r"\d+(?:\.\d+)?", " ".join(w["word"] for w in SOURCE)))
    # Numbers on screen must come from the speech; add style-neutral ones in plan["allowed_numbers"].
    allowed = spoken | {str(x) for x in PLAN.get("allowed_numbers", [])}
    numbers = set(re.findall(r"\d+(?:\.\d+)?", text))
    assert numbers <= allowed, numbers - allowed
