#!/usr/bin/env python3
"""Count a benchmark run's verdicts against each input's reference.md, and how far repeated runs agree.

Usage: python3 evals/verify-spec/benchmark/score.py <label> [input ...]

Reads the replies bench.py saved in evals/verify-spec/runs/bench-<label>/: <input>.md, or <input>-r1.md,
<input>-r2.md, ... from a run with --runs. For each input it prints one line per requirement with the
reference's verdict and each run's, then the counts the README defines: verdicts right, gaps missed, false
alarms, drift right, and the rows on which every run gave the same verdict. A reference row that names two
verdicts ("met or partial") is an open row: either is right, and only its agreement says anything.

The counting is mechanical. Reading why a row is wrong, and whether a reply's evidence names the planted
cause, is still done by hand. Python 3 standard library only.
"""

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("parse_reply", ROOT / "skills" / "build-phase" / "scripts" / "parse_reply.py")
parse_reply = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse_reply)

GAPS = {"partial", "unmet", "untested"}
REFERENCE_ROW = re.compile(r"^\| ((?:FR|NFR)-\d+) \| ([^|]+) \|", re.M)
NOT_CHECKED = "not checked (no feature branch)"


def read_reference(text):
    """{"rows": {ID: [the verdicts that are right]}, "drift": [paths], or the Drift line's own words}."""
    rows = {}
    for req, cell in REFERENCE_ROW.findall(text):
        verdicts = [v.strip() for v in cell.split(" or ")]
        if all(v in parse_reply.VERDICTS for v in verdicts):
            rows[req] = verdicts
    drift = re.search(r"^Expected drift: `([^`]+)`", text, re.M)
    drift = drift.group(1) if drift else "none"
    return {"rows": rows, "drift": drift if drift in (NOT_CHECKED, "none") else drift.split(", ")}


def score(reference, reply):
    """One reply's counts. verdicts maps each reference ID to the reply's verdict, or None for a missing row."""
    parsed = parse_reply.parse_verify(reply)
    rows = {r["id"]: r["verdict"] for r in parsed.get("rows", [])}
    verdicts = {req: rows.get(req) for req in reference["rows"]}
    # A reply the parser rejects (the report written twice, say) still has a Drift line to count: the last one.
    drift = parsed.get("drift") or next((l[7:] for l in reversed(parse_reply.lines_of(reply)) if l.startswith("Drift: ")), None)
    listed = [] if drift in (None, "none", NOT_CHECKED) else [p.strip() for p in drift.split(",")]
    expected = reference["drift"]
    if isinstance(expected, list):
        drift_right = sorted(listed) == sorted(expected)
        extra = [p for p in listed if p not in expected]
    else:
        drift_right = drift == expected
        extra = listed
    strict = parse_reply.parse_verify(reply, strict=True)
    return {
        "verdicts": verdicts,
        "right": sum(1 for req, v in verdicts.items() if v in reference["rows"][req]),
        "gaps_missed": [req for req, v in verdicts.items() if v == "met" and set(reference["rows"][req]) <= GAPS],
        "false_alarms": [req for req, v in verdicts.items() if v not in (None, "met") and reference["rows"][req] == ["met"]] + extra,
        "drift": drift,
        "drift_right": drift_right,
        "problems": strict["problems"] if strict["kind"] == "invalid" else [],
    }


def agreeing(reference, scores):
    """The IDs on which every run gave the same verdict."""
    return [req for req in reference["rows"] if len({s["verdicts"][req] for s in scores}) == 1]


def replies_of(run_dir, name):
    """An input's replies, in run order: <name>-r1.md, <name>-r2.md, ..., or the single <name>.md."""
    numbered = sorted(run_dir.glob(f"{name}-r*.md"), key=lambda p: int(p.stem.rsplit("-r", 1)[1]))
    single = run_dir / f"{name}.md"
    return numbered or ([single] if single.is_file() else [])


def report(name, reference, scores):
    """The lines for one input, and its totals as a dict."""
    ids = list(reference["rows"])
    gaps = [req for req in ids if set(reference["rows"][req]) <= GAPS]
    same = agreeing(reference, scores)
    lines = [f"== {name}", "| ID | Reference | " + " | ".join(f"Run {i}" for i in range(1, len(scores) + 1)) + " |"]
    for req in ids:
        cells = [s["verdicts"][req] or "no row" for s in scores]
        mark = "" if req in same else "  <- runs differ"
        lines.append(f"| {req} | {' or '.join(reference['rows'][req])} | " + " | ".join(cells) + f" |{mark}")
    for i, s in enumerate(scores, 1):
        lines.append(f"Run {i}: {s['right']} of {len(ids)} right, {len(s['gaps_missed'])} of {len(gaps)} gaps missed"
                     + (f" ({', '.join(s['gaps_missed'])})" if s["gaps_missed"] else "")
                     + f", {len(s['false_alarms'])} false alarms"
                     + (f" ({', '.join(s['false_alarms'])})" if s["false_alarms"] else "")
                     + f", drift {'right' if s['drift_right'] else 'wrong'}: {s['drift']}"
                     + (f"; contract: {'; '.join(s['problems'])}" if s["problems"] else ""))
    if len(scores) > 1:
        lines.append(f"Agreement: {len(same)} of {len(ids)} rows the same in every run")
    totals = {
        "rows": len(ids) * len(scores), "right": sum(s["right"] for s in scores),
        "gaps": len(gaps) * len(scores), "gaps_missed": sum(len(s["gaps_missed"]) for s in scores),
        "false_alarms": sum(len(s["false_alarms"]) for s in scores),
        "runs": len(scores), "drift_right": sum(s["drift_right"] for s in scores),
        "ids": len(ids), "same": len(same),
    }
    return lines, totals


def total_line(label, totals):
    line = (f"{label}: {totals['right']} of {totals['rows']} right, {totals['gaps_missed']} of {totals['gaps']} gaps missed, "
            f"{totals['false_alarms']} false alarms, drift right in {totals['drift_right']} of {totals['runs']} runs")
    # With one run per input there is nothing to agree with.
    return line + (f", {totals['same']} of {totals['ids']} rows the same in every run" if totals["rows"] > totals["ids"] else "")


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    run_dir = HERE.parent / "runs" / f"bench-{argv[0]}"
    names = argv[1:] or sorted(p.name for p in HERE.iterdir() if (p / "reference.md").is_file())
    sums = {}
    for name in names:
        replies = replies_of(run_dir, name)
        if not replies:
            print(f"== {name}\nno reply in {run_dir.relative_to(ROOT)}/")
            continue
        reference = read_reference((HERE / name / "reference.md").read_text())
        lines, totals = report(name, reference, [score(reference, p.read_text()) for p in replies])
        print("\n".join(lines) + "\n")
        for group in (name.split("-")[0], "all"):
            sums[group] = {k: sums.get(group, {}).get(k, 0) + v for k, v in totals.items()}
    for group in sorted(sums, key=lambda g: (g == "all", g)):
        print(total_line(group, sums[group]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
