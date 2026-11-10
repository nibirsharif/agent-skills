#!/usr/bin/env python3
"""Run a skill's benchmark inputs through the agent once each and save the replies. Nothing is graded here.

Usage: python3 evals/bench.py <skill> [input ...] [--model M] [--label NAME] [--file turn2.md]

Inputs are evals/<skill>/benchmark/<name>/input.md, or the file --file names in the same folder (turn2.md is
the input, a fixed first reply, and scripted answers). Each has a reference.md beside it, which the agent never
sees: the decisions the input leaves open. Replies go to evals/<skill>/runs/bench-<label>/<name>.md, with the
run's cost in <name>.json. See evals/<skill>/benchmark/README.md for how the replies are scored.
"""

import argparse
import json
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import grading
import run


def one(skill, config, name, source, out, model):
    prompt = config["prompt"].replace("{input}", source.read_text())
    with tempfile.TemporaryDirectory(prefix=f"{skill}-bench-") as tmp:
        tmp = Path(tmp)
        (tmp / "work").mkdir()
        cmd = run.default_agent(config, run.build_plugin(skill, tmp / "plugin"), model) + [prompt]
        code, stdout, stderr = run.run_command(cmd, tmp / "work", run.DEFAULT_TIMEOUT)
    if code != 0:
        out.with_suffix(".err").write_text(stderr or stdout)
        return f"FAIL  {name}: {run.agent_error(stdout, stderr)}"
    events = [json.loads(line) for line in stdout.splitlines() if line.strip().startswith("{")]
    result = grading.summarize(events, config.get("watch", []))["result"]
    out.write_text(result.get("result", ""))
    out.with_suffix(".json").write_text(json.dumps({k: v for k, v in result.items() if k != "result"}, indent=2))
    return f"ok    {name}: ${result.get('total_cost_usd', 0):.2f}"


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1])
    parser.add_argument("skill")
    parser.add_argument("inputs", nargs="*")
    parser.add_argument("--model")
    parser.add_argument("--file", default="input.md")
    parser.add_argument("--label", default=time.strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args(argv)

    here = grading.EVALS / args.skill
    config = json.loads((here / "config.json").read_text())
    names = args.inputs or sorted(p.name for p in (here / "benchmark").iterdir() if (p / args.file).is_file())
    out_dir = here / "runs" / f"bench-{args.label}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Started {len(names)} runs. Replies go to {out_dir.relative_to(run.ROOT)}/")
    with ThreadPoolExecutor(max_workers=len(names)) as pool:
        jobs = [pool.submit(one, args.skill, config, n, here / "benchmark" / n / args.file,
                            out_dir / f"{n}.md", args.model) for n in names]
        lines = [job.result() for job in jobs]
    print("\n".join(lines))
    return 1 if any(line.startswith("FAIL") for line in lines) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
