"""Helpers shared by the research scripts: positions with their sources, and
recorded congressional votes as sources.

A position is (question id, stance, source, short quote or None). The stance
scale is the site's: 2 strongly supports ... -2 strongly opposes. A question with
no clear public position is left out, never inferred from party.
"""

import json
import sys
from pathlib import Path

TODAY = "2026-10-24"
ROOT = Path(__file__).resolve().parents[2]


def source(title, url, date):
    s = {"title": title, "url": url, "date": date}
    if date == TODAY:
        s["accessed"] = True  # a live page: the date is when it was read
    return s


def P(*rows):
    out = {}
    for qid, stance, src, quote in rows:
        assert qid not in out, qid
        assert stance in (-2, -1, 0, 1, 2), (qid, stance)
        s = dict(src)
        if quote:
            assert len(quote.split()) <= 25, quote
            s["quote"] = quote
        out[qid] = {"stance": stance, "source": s}
    return out


# Recorded House votes: the definitions and the vote-to-question rules live with
# the automatic pipeline, so hand-researched and automatic members match exactly.
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
from house_votes import HOUSE_VOTES, house_vote, vote_positions  # noqa: E402,F401


def write(path, races, note):
    out = {"updated": TODAY, "note": note, "races": races}
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(c.get("positions", {})) for r in races for c in r.get("candidates", []))
    print(f"wrote {path}: {len(races)} races, {sum(len(r.get('candidates', [])) for r in races)} candidates, {n} sourced positions")
