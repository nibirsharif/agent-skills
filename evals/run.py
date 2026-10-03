#!/usr/bin/env python3
"""Run a skill's eval cases through an agent, in parallel, and grade each reply.

Usage: python3 evals/run.py <skill> [case ...] [options]    (no case: run them all)

Options:
  --model M       model for the default agent, for example sonnet or haiku (default: the CLI's default)
  --runs N        run each case N times (default 1), to see how much results vary
  --judge         also grade each case's "expectations" with an LLM judge (one more call per run)
  --judge-model M model for the judge (default: the CLI's default)
  --agent CMD     use another agent command; it gets the prompt as its last argument. Checks that
                  need a transcript (fires, target "trace") are then reported as skipped.

The default agent is `claude -p` with this repo's released skills plus the skill under test loaded
as a plugin, and the tools from evals/<skill>/config.json allowed without prompting. Each run starts
in an empty folder, so no project config or files affect it, unless config.json names a "fixture"
folder: it is copied in and committed as a git repository on main, and a case's dirty/ folder is then
copied over it uncommitted. All runs start at once, so a full run
takes about as long as the slowest case.

Replies, transcripts (.jsonl), stats (.json), judge results (.judge.json) and error output (.err)
are saved in evals/<skill>/runs/, which git ignores. Exits 1 when any run fails.
"""

import argparse
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import grading

ROOT = grading.EVALS.parent
DEFAULT_TIMEOUT = 600


def build_plugin(skill, into):
    """A plugin folder that loads the released skills plus the skill under test.

    The skills are copied: Claude Code refuses a plugin skill that is a symlink out of the plugin folder.
    """
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    names = {Path(p).name for p in manifest.get("skills", [])} | {skill}
    (into / ".claude-plugin").mkdir(parents=True)
    (into / "skills").mkdir()
    for name in sorted(names):
        shutil.copytree(ROOT / "skills" / name, into / "skills" / name)
    manifest["skills"] = [f"./skills/{name}" for name in sorted(names)]
    (into / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2))
    return into


def default_agent(config, plugin, model):
    # --allowedTools and --add-dir take lists, so a flag with a single value must follow them;
    # otherwise the prompt (the last argument) would be read as one more list item.
    cmd = ["claude", "-p", "--plugin-dir", str(plugin),
           "--add-dir", str(plugin),
           "--allowedTools", "Skill", *config.get("allowed_tools", []),
           "--no-session-persistence", "--output-format", "stream-json", "--verbose"]
    return cmd + (["--model", model] if model else [])


def run_command(cmd, cwd, limit, stdin=""):
    """Run cmd with a time limit. Returns (exit code or None on timeout, stdout, stderr)."""
    proc = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(stdin, timeout=limit)
        return proc.returncode, out, err
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)  # the agent's own child processes too
        out, err = proc.communicate()
        return None, out, err


def judge(task, reply, expectations, model, cwd):
    """Ask an LLM to grade the reply against the expectations. Returns (results, errors)."""
    cmd = ["claude", "-p", "--tools", "", "--no-session-persistence", "--output-format", "json",
           "--json-schema", json.dumps(grading.JUDGE_SCHEMA)] + (["--model", model] if model else [])
    # The prompt goes on stdin: a long reply could pass the OS limit for arguments.
    code, out, err = run_command(cmd, cwd, 300, grading.judge_prompt(task, reply, expectations))
    if code != 0:
        return [], [f"judge exited with {code}: {(err or out).strip()[:200]}"]
    try:
        result = json.loads(out)
    except ValueError:
        return [], [f"judge output is not JSON: {out[:200]}"]
    if result.get("is_error"):
        return [], [f"judge failed: {str(result.get('result'))[:200]}"]
    return grading.parse_judgement(result.get("structured_output") or result.get("result", ""), expectations)


def agent_error(stdout, stderr):
    """The most useful line explaining why an agent run failed."""
    for line in reversed(stdout.splitlines()):
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "result" and event.get("result"):
            return str(event["result"])[:300]
    lines = (stderr or stdout).strip().splitlines()
    return lines[-1][:300] if lines else "no output"


def prepare_work(fixture, case_dir, work):
    """Fill the agent's folder: the skill's fixture (config.json "fixture") becomes a git repository with
    one commit on main, then the case's dirty/ is copied over it uncommitted. Without a fixture, the
    folder starts empty."""
    if fixture:
        shutil.copytree(fixture, work, dirs_exist_ok=True)
        git = ["git", "-c", "user.name=Eval", "-c", "user.email=eval@example.com", "-c", "commit.gpgsign=false"]
        for cmd in (["git", "init", "-q", "-b", "main"], ["git", "add", "-A"], git + ["commit", "-q", "-m", "Initial commit"]):
            subprocess.run(cmd, cwd=work, check=True, capture_output=True)
    dirty = case_dir / "dirty"
    if dirty.is_dir():
        shutil.copytree(dirty, work, dirs_exist_ok=True)


def run_case(skill, case_dir, config, out, args):
    """Run one case once. Returns (passed, report lines)."""
    checks = json.loads((case_dir / "checks.json").read_text())
    limit = checks.get("timeout_seconds", DEFAULT_TIMEOUT)
    text = (case_dir / "input.md").read_text()
    # A routing case is sent as a user would type it: the template names the skill.
    prompt = text if "fires" in checks else config["prompt"].replace("{input}", text)
    report, rel = [], out.relative_to(ROOT)

    with tempfile.TemporaryDirectory(prefix=f"{skill}-eval-") as tmp:
        tmp = Path(tmp)
        (tmp / "work").mkdir()
        fixture = config.get("fixture")
        prepare_work(grading.EVALS / skill / fixture if fixture else None, case_dir, tmp / "work")
        if args.agent:
            cmd = shlex.split(args.agent) + [prompt]
        else:
            cmd = default_agent(config, build_plugin(skill, tmp / "plugin"), args.model) + [prompt]
        started = time.time()
        code, stdout, stderr = run_command(cmd, tmp / "work", limit)
        if stderr.strip():
            out.with_suffix(".err").write_text(stderr)
        if code != 0:
            out.write_text(stdout)
            why = f"passed the {limit}s limit" if code is None else f"exited with {code}"
            return False, [f"FAIL agent {why}: {agent_error(stdout, stderr)}", f"   output: {rel}"]

        trace = None
        if args.agent:
            reply = stdout
        else:
            events = [json.loads(line) for line in stdout.splitlines() if line.strip().startswith("{")]
            trace = grading.summarize(events, config.get("watch", []))
            out.with_suffix(".jsonl").write_text(stdout)
            result = trace["result"]
            reply = result.get("result", "")
            stats = {k: v for k, v in result.items() if k != "result"}
            stats.update(watch_ran=trace["watch_ran"], watch_blocked=trace["watch_blocked"], skills=trace["skills"])
            out.with_suffix(".json").write_text(json.dumps(stats, indent=2))
            watched = ", ".join(config.get("watch", [])) or "watched commands"
            report.append(f"   {result.get('num_turns', '?')} turns, {time.time() - started:.0f}s, "
                          f"${result.get('total_cost_usd', 0):.2f}, {watched} ran {trace['watch_ran']}x"
                          + (f" ({trace['watch_blocked']} blocked)" if trace["watch_blocked"] else "")
                          + (f", skills: {', '.join(trace['skills'])}" if trace["skills"] else ""))
        out.write_text(reply)
        report.append(f"   reply: {rel}")

        failures, skipped, manual = grading.grade(case_dir, reply, trace)
        # A plugin that failed to load means the skill under test may be missing: the run proves nothing.
        failures += [f"plugin failed to load: {e}" for e in (trace or {}).get("plugin_errors", [])]
        report += [f"FAIL {f}" for f in failures] + [f"SKIP {s}" for s in skipped]

        expectations = checks.get("expectations", [])
        if args.judge and expectations:
            results, errors = judge(prompt, reply, expectations, args.judge_model, tmp / "work")
            out.with_suffix(".judge.json").write_text(json.dumps({"results": results, "errors": errors}, indent=2))
            failures += [f"judge: {e}" for e in errors]
            report += [f"FAIL judge: {e}" for e in errors]
            for r in results:
                report.append(f"{'PASS' if r['passed'] else 'FAIL'} judge {r['id']}: {r['expectation']}")
                if not r["passed"]:
                    failures.append(r["expectation"])
                    report.append(f"    {r['evidence'][:200]}")

    if manual:
        report += ["", "Review by hand:"] + [f"- [ ] {item}" for item in manual]
    return not failures, report


def main(argv):
    parser = argparse.ArgumentParser(usage=__doc__.split("\n\n")[1])
    parser.add_argument("skill")
    parser.add_argument("cases", nargs="*")
    parser.add_argument("--model")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--judge-model")
    parser.add_argument("--agent")
    args = parser.parse_args(argv)

    here = grading.EVALS / args.skill
    if not (here / "config.json").is_file():
        parser.error(f"{here.relative_to(ROOT)}/config.json not found")
    config = json.loads((here / "config.json").read_text())
    names = args.cases or sorted(p.name for p in (here / "cases").iterdir() if p.is_dir())
    missing = [n for n in names if not (here / "cases" / n / "checks.json").is_file()]
    if missing:
        parser.error(f"no such case: {', '.join(missing)}")

    installed = Path.home() / ".claude" / "skills" / args.skill
    if not args.agent and installed.is_symlink() and installed.resolve() == (ROOT / "skills" / args.skill).resolve():
        print(f"warning: {installed} links to this repo, so the skill loads twice and routing results"
              " are less reliable. Run `make uninstall` for a clean run.\n")

    (here / "runs").mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    suffix = f"-{args.model}" if args.model else ""
    jobs = [(n, i, here / "runs" / f"{n}-{stamp}-r{i}{suffix}.md") for n in names for i in range(1, args.runs + 1)]
    print(f"Started {len(jobs)} runs{' on ' + args.model if args.model else ''}. Waiting...")

    with ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        futures = [pool.submit(run_case, args.skill, here / "cases" / n, config, out, args) for n, _, out in jobs]
        outcomes = []
        for (name, i, _), future in zip(jobs, futures):
            try:
                passed, report = future.result()
            except Exception as e:  # report a broken run and keep the others
                passed, report = False, [f"FAIL runner error: {e!r}"]
            outcomes.append((f"{name} run {i}", passed))
            print(f"\n== {name} run {i}")
            print("\n".join(report))

    print(f"\n== Summary{' (' + args.model + ')' if args.model else ''}")
    for label, passed in outcomes:
        print(f"{'PASS' if passed else 'FAIL'}  {label}")
    return 0 if all(p for _, p in outcomes) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
