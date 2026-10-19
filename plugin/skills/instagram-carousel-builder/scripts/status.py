#!/usr/bin/env python3
"""
status.py - read a carousel's stage, or move it and log why.

Stages
  designed             design.md written and the no-repeat check passed; copy and slides next
  rendered             slides rendered and measured; ready for the check
  needs_fix            the check said FIX; fix list in check/round-N.md
  awaiting_approval    the check said PASS; Human check 2
  needs_human          failed the last allowed round; a person decides
  approved             approved for Publish

render.py and score.py move the stage themselves. Use this for the moves in between
(designed, approver notes).

status.json
  {"slug": "...", "stage": "...", "round": 1, "verdict": "FIX", "score": 3.4,
   "updated": "...", "approver_notes": [...],
   "history": [{"at": "...", "event": "questions_sent", "stage": "waiting_on_designer", "note": "..."}]}

Usage
  python3 status.py carousels/<slug>
  python3 status.py carousels/<slug> designed --event designed --note "mix of swiss-grid + zine"
  python3 status.py carousels/<slug> needs_fix --event approver_notes --note "Cover: lead with the cost instead"
  python3 status.py carousels/<slug> --event note --note "cover headline cut to 8 words"   # log only, stage unchanged
"""

import argparse
import datetime as dt
import json
import os
import sys

STAGES = ["designed", "rendered", "needs_fix", "awaiting_approval", "needs_human", "approved"]


def main():
    ap = argparse.ArgumentParser(description="Read or move a carousel's stage.")
    ap.add_argument("carousel")
    ap.add_argument("stage", nargs="?", choices=STAGES)
    ap.add_argument("--event", help="short event name, e.g. designed, fixed, approver_notes")
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    path = os.path.join(os.path.abspath(args.carousel), "status.json")
    st = json.load(open(path, encoding="utf-8")) if os.path.isfile(path) else {}
    if not args.stage and not args.event:
        print(json.dumps(st, indent=2, ensure_ascii=False) if st else "no status.json yet")
        return
    at = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    st["slug"] = os.path.basename(os.path.abspath(args.carousel))
    if args.stage:
        st["stage"] = args.stage
    args.stage = st.get("stage")
    st["updated"] = at
    if args.event == "approver_notes" and args.note:
        st.setdefault("approver_notes", []).append(args.note)
    st.setdefault("history", []).append({"at": at, "event": args.event or "stage", "stage": args.stage, "note": args.note})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"{st['slug']}: {args.stage}" + (f" ({args.event})" if args.event else ""))


if __name__ == "__main__":
    sys.exit(main())
