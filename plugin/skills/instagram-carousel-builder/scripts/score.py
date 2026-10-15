#!/usr/bin/env python3
"""
score.py - turn the judge's line scores into a verdict, the same way every time.

The judge (Claude, looking at the slides) scores each rubric line 1-5 with a
reason and slide-level evidence. This script does everything that should not be
left to judgement:

  1. re-runs lint.py so the facts are current
  2. caps each line at whatever the lint findings allow (rubric.json "caps")
  3. weighted average with rubric.json weights
  4. pass rule: weighted average >= 4.0 AND no line below 3
  5. verdict: PASS -> awaiting human approval
              FIX  -> fix list goes back to the make workflow
              ESCALATE -> failed the last allowed round, a person decides
  6. writes check/round-N.json + check/round-N.md and updates status.json

Usage
  python3 score.py carousels/<slug> --judge carousels/<slug>/check/judge-r1.json
  python3 score.py carousels/<slug> --approve "Name"     # record Human check 2
"""

import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lint  # noqa: E402

EVIDENCE_RE = re.compile(r"\bslides?\s*\d+|\b\d{1,2}\s*/\s*\d{1,2}\b|\bS\d+\b", re.IGNORECASE)
CAPTION_RE = re.compile(r"\bcaption\b", re.IGNORECASE)


def line_min(rubric, line_id):
    """Pass minimum for one line: the general line_min, or a stricter per-line one (e.g. share: 4)."""
    pr = rubric["pass"]
    return max(pr["line_min"], (pr.get("line_mins") or {}).get(line_id, 0))


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def load(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def validate(judge, rubric):
    errs = []
    lines = judge.get("lines") or {}
    for ln in rubric["lines"]:
        j = lines.get(ln["id"])
        if not j:
            errs.append(f"missing line '{ln['id']}'")
            continue
        sc = j.get("score")
        if not isinstance(sc, int) or not 1 <= sc <= 5:
            errs.append(f"{ln['id']}: score must be an integer 1-5 (got {sc!r})")
        if not (j.get("reason") or "").strip():
            errs.append(f"{ln['id']}: reason is empty")
        if ln.get("evidence") == "caption":
            if not CAPTION_RE.search(j.get("evidence") or ""):
                errs.append(f"{ln['id']}: evidence must quote the caption (e.g. 'Caption line 1: ...')")
        elif not EVIDENCE_RE.search(j.get("evidence") or ""):
            errs.append(f"{ln['id']}: evidence must point at slide numbers (e.g. 'Slide 3: ...')")
        if isinstance(sc, int) and sc < 5 and not (j.get("to_reach_5") or "").strip():
            errs.append(f"{ln['id']}: scored below 5 but 'to_reach_5' is empty")
    # gate rulings the judge owns (the ones you can only see: dead space, visible overlaps, a logo, decoration)
    jg = judge.get("gates") or {}
    for g in rubric.get("gates") or []:
        if not g.get("judge"):
            continue
        r = jg.get(g["id"])
        if not isinstance(r, dict) or not isinstance(r.get("pass"), bool):
            errs.append(f"gates.{g['id']} ({g['name']}): needs {{\"pass\": true|false, \"evidence\": \"...\"}}")
        elif r["pass"] is False and not EVIDENCE_RE.search(r.get("evidence") or ""):
            errs.append(f"gates.{g['id']}: a failed gate needs evidence naming the slide")
    risks = judge.get("risks")
    if not isinstance(risks, list) or not 3 <= len(risks) <= 5:
        errs.append("risks: give 3-5 honest reasons this might NOT get engagement, each {\"reason\", \"fix\"}")
    extra = set(lines) - {ln["id"] for ln in rubric["lines"]}
    if extra:
        errs.append(f"unknown line(s): {', '.join(sorted(extra))}")
    return errs


def lint_fixes(lint_out):
    """Turn lint errors/warnings that cap a line into fix notes for the make workflow."""
    out = []
    for f in lint_out["findings"]:
        if f["severity"] in ("error", "warn") and f["cap"] is not None:
            out.append({"slide": f["slide"], "line": f["line"], "note": f["message"], "from": "lint"})
    return out


def render_md(card):
    r = card
    lines = [
        f"# Check · {r['slug']} · round {r['round']} · {r['verdict']}",
        "",
        f"**Weighted score {r['weighted']:.2f} / 5 ({round(r['weighted'] * 20)}/100)** (pass: every gate, {r['pass_rule']['weighted_avg_min']}+ and no line below "
        f"{r['pass_rule']['line_min']}"
        + "".join(f", {next((l['name'] for l in r['lines'] if l['id'] == k), k)} at {v}+"
                  for k, v in (r['pass_rule'].get('line_mins') or {}).items())
        + f") · rubric v{r['rubric_version']} · judged by {r['judge']}",
        "",
    ]
    if r.get("gates"):
        failed = [g for g in r["gates"] if not g["pass"]]
        lines += [("**Gates: all passed.**" if not failed else
                   f"**Gates: {len(failed)} failed ({', '.join(g['id'] for g in failed)}), so this can't pass until they're fixed.**"), "",
                  "| Gate | Result | Evidence |", "|---|---|---|"]
        for g in r["gates"]:
            lines.append(f"| {g['id']} {g['name']} | {'✅' if g['pass'] else '❌'} | {(g['evidence'] or '').replace('|', '/')} |")
        lines.append("")
    if not r.get("rubric_calibrated"):
        lines += ["> Rubric not yet calibrated against past posts, so treat the 4.0 bar as provisional "
                  "(references/calibration.md).", ""]
    lines += [
        "| Line | Weight | Judge | Cap | Final | Why |",
        "|---|---|---|---|---|---|",
    ]
    for ln in r["lines"]:
        cap = str(ln["cap"]) if ln["cap"] is not None else "—"
        flag = " ⚠" if ln["final"] < max(r["pass_rule"]["line_min"], (r["pass_rule"].get("line_mins") or {}).get(ln["id"], 0)) else ""
        why = ln["reason"]
        if ln.get("capped_by"):
            why += f" · capped at {ln['cap']} by lint: " + "; ".join(ln["capped_by"])
        lines.append(f"| {ln['name']} | {int(ln['weight'] * 100)}% | {ln['judge']} | {cap} | **{ln['final']}**{flag} | "
                     f"{why.replace('|', '/')} |")
    if r.get("summary"):
        lines += ["", r["summary"]]
    if r["fixes"]:
        heading = {"FIX": "## Fix list (for the make workflow)",
                   "PASS": "## Optional polish (not needed to pass; the approver decides)",
                   "ESCALATE": "## Still failing"}[r["verdict"]]
        lines += ["", heading]
        for k, f in enumerate(r["fixes"], 1):
            where = f"Slide {f['slide']}" if f.get("slide") else ("Caption" if f.get("line") == "caption" else "Whole carousel")
            lines.append(f"{k}. **{where} · {f.get('line', '')}**: {f['note']}")
    if r.get("risks"):
        lines += ["", "## Why might this NOT get engagement?"]
        for k in r["risks"]:
            lines.append(f"- {k.get('reason', '')} → {k.get('fix', '')}")
    other = [f for f in r["lint"]["findings"] if f["severity"] in ("error", "warn") and f["cap"] is None]
    if other:
        lines += ["", "## Other lint notes (don't cap the score)"]
        for f in other:
            where = f"slide {f['slide']}" if f["slide"] else "carousel"
            lines.append(f"- {where}: {f['message']}")
    if r["verdict"] == "PASS":
        lines += ["", "Next: Human check 2. The approver looks at `board.png` and this scorecard, then records the "
                  "decision with `score.py <carousel> --approve \"Name\"`."]
    elif r["verdict"] == "ESCALATE":
        lines += ["", f"Failed round {r['round']} of {r['max_rounds']}. A person decides: approve as is, edit by hand, "
                  "or kill. Don't run another automatic round."]
    return "\n".join(lines) + "\n"


def approve(cdir, who):
    sp = os.path.join(cdir, "status.json")
    st = load(sp, {}) or {}
    if st.get("verdict") != "PASS" and st.get("stage") != "needs_human":
        sys.exit(f"Last check verdict is {st.get('verdict')!r}; only PASS (or an escalated carousel) can be approved.")
    st.update({"stage": "approved", "approved_by": who, "approved_at": now(), "updated": now()})
    st.setdefault("history", []).append({"at": now(), "event": "approved", "by": who})
    save(sp, st)
    print(f"approved by {who}")


def main():
    ap = argparse.ArgumentParser(description="Score a carousel from the judge's rubric scores.")
    ap.add_argument("carousel")
    ap.add_argument("--judge", help="judge JSON (default: newest check/judge-r*.json)")
    ap.add_argument("--approve", metavar="NAME", help="record the human approval instead of scoring")
    args = ap.parse_args()
    cdir = os.path.abspath(args.carousel)

    if args.approve:
        return approve(cdir, args.approve)

    rubric = lint.load(lint.RUBRIC)
    jpath = args.judge
    if not jpath:
        cands = sorted(glob.glob(os.path.join(cdir, "check", "judge-r*.json")), key=os.path.getmtime)
        if not cands:
            sys.exit("No judge file. Write check/judge-rN.json first (see references/rubric.md).")
        jpath = cands[-1]
    judge = load(jpath)
    if judge is None:
        sys.exit(f"Can't read {jpath}")

    lint_out = lint.run(cdir)
    if lint_out["counts"]["fatal"]:
        print(lint.summary(lint_out))
        sys.exit("Blocked by fatal lint findings; fix those (usually: re-render) before scoring.")

    errs = validate(judge, rubric)
    if errs:
        sys.exit("Judge file is incomplete:\n  - " + "\n  - ".join(errs))

    prior = sorted(glob.glob(os.path.join(cdir, "check", "round-*.json")))
    rnd = len(prior) + 1  # the script owns the round number, never the judge
    if judge.get("round") and int(judge["round"]) != rnd:
        sys.exit(f"Judge file says round {judge['round']} but this is round {rnd}. Re-run the judge for round {rnd}.")
    weights = {ln["id"]: ln["weight"] for ln in rubric["lines"]}
    if abs(sum(weights.values()) - 1) > 0.001:
        sys.exit("rubric.json weights don't add up to 1.0")

    rows, total = [], 0.0
    for ln in rubric["lines"]:
        j = judge["lines"][ln["id"]]
        cap = lint_out["caps"].get(ln["id"])
        final = min(j["score"], cap) if cap is not None else j["score"]
        total += ln["weight"] * final
        capped_by = [(f"slide {f['slide']}: " if f["slide"] else "") + f["message"].rstrip(".") for f in lint_out["findings"]
                     if f["line"] == ln["id"] and f["cap"] is not None and f["cap"] == cap and cap < j["score"]]
        rows.append({"id": ln["id"], "name": ln["name"], "weight": ln["weight"], "judge": j["score"], "cap": cap,
                     "final": final, "reason": j["reason"], "evidence": j["evidence"],
                     "to_reach_5": j.get("to_reach_5", ""), "capped_by": capped_by})
    weighted = round(total, 2)
    pr = rubric["pass"]
    # Gates: lint's measured failures plus the judge's rulings. Any failed gate blocks a pass.
    gate_rows = []
    for g in rubric.get("gates") or []:
        lint_fail = lint_out.get("gates_failed", {}).get(g["id"]) or []
        jr = (judge.get("gates") or {}).get(g["id"]) or {}
        judge_fail = g.get("judge") and jr.get("pass") is False
        gate_rows.append({"id": g["id"], "name": g["name"], "pass": not (lint_fail or judge_fail),
                          "evidence": "; ".join(lint_fail + ([jr.get("evidence", "")] if judge_fail else [])) or jr.get("evidence", "")})
    gates_ok = all(gr["pass"] for gr in gate_rows)
    passed = gates_ok and weighted >= pr["weighted_avg_min"] and all(r["final"] >= line_min(rubric, r["id"]) for r in rows)
    verdict = "PASS" if passed else ("FIX" if rnd < rubric["max_rounds"] else "ESCALATE")

    # One fix per (slide, line): lint's fact first, then the judge's suggested change.
    grouped = {}
    for f in lint_fixes(lint_out) + [dict(f, **{"from": "judge"}) for f in judge.get("fixes") or []]:
        key = (f.get("slide"), f.get("line"))
        g = grouped.setdefault(key, {"slide": f.get("slide"), "line": f.get("line"), "notes": [], "from": []})
        if f["note"] not in g["notes"]:
            g["notes"].append(f["note"])
            g["from"].append(f.get("from", "judge"))
    fixes = [{"slide": g["slide"], "line": g["line"], "note": " · ".join(n.rstrip(".") for n in g["notes"]) + ".",
              "from": "+".join(dict.fromkeys(g["from"]))}
             for g in grouped.values()]
    fixes.sort(key=lambda f: (f.get("slide") or 0, f.get("line") or ""))

    card = {
        "slug": os.path.basename(cdir), "round": rnd, "verdict": verdict, "weighted": weighted,
        "pass_rule": pr, "max_rounds": rubric["max_rounds"], "rubric_version": rubric["version"],
        "rubric_calibrated": bool(rubric.get("calibrated")),
        "judge": judge.get("judge", "unspecified"), "judge_file": os.path.relpath(jpath, cdir),
        "scored_at": now(), "lines": rows, "summary": judge.get("summary", ""), "fixes": fixes, "lint": lint_out,
        "gates": gate_rows, "gates_ok": gates_ok, "risks": judge.get("risks") or [],
    }
    save(os.path.join(cdir, "check", f"round-{rnd}.json"), card)
    md = render_md(card)
    with open(os.path.join(cdir, "check", f"round-{rnd}.md"), "w", encoding="utf-8") as f:
        f.write(md)

    sp = os.path.join(cdir, "status.json")
    st = load(sp, {}) or {}
    st["slug"] = card["slug"]
    st.update({"stage": {"PASS": "awaiting_approval", "FIX": "needs_fix", "ESCALATE": "needs_human"}[verdict],
               "round": rnd, "verdict": verdict, "score": weighted, "updated": now()})
    st.setdefault("history", []).append({"at": now(), "event": "checked", "round": rnd, "verdict": verdict, "score": weighted})
    save(sp, st)
    print(md)


if __name__ == "__main__":
    main()
