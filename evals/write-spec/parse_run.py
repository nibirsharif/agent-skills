#!/usr/bin/env python3
"""Split a `claude -p --output-format stream-json --verbose` run into reply, stats, and transcript.

Usage: python3 parse_run.py <run-file.md>

The run file holds the raw stream (one JSON event per line) when called. Afterwards:
- <run>.md     the final reply, for grading
- <run>.jsonl  the full transcript
- <run>.json   the result stats, plus how often the lint ran and how often it was blocked

Prints one summary line. Leaves the file alone when it is not a stream (another agent's plain text).
"""

import json
import sys
from pathlib import Path


def summarize(events):
    """Return (result event, lint runs that returned output, lint calls that were blocked or failed)."""
    calls, result = {}, {}
    ran = blocked = 0
    for event in events:
        # Some events carry a plain string as "message" (for example system/permission_denied).
        message = event.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        content = [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []
        if event.get("type") == "assistant":
            for block in content:
                if block.get("type") == "tool_use" and "lint.py" in json.dumps(block.get("input", {})):
                    calls[block["id"]] = block
        elif event.get("type") == "user":
            for block in content:
                if block.get("type") == "tool_result" and block.get("tool_use_id") in calls:
                    if block.get("is_error"):
                        blocked += 1
                    else:
                        ran += 1
        elif event.get("type") == "result":
            result = event
    return result, ran, blocked


def main(argv):
    if len(argv) != 1:
        print(__doc__.strip())
        return 2
    path = Path(argv[0])
    raw = path.read_text()
    try:
        events = [json.loads(line) for line in raw.splitlines() if line.strip()]
    except ValueError:
        return 0  # not a stream: grade the raw output
    result, ran, blocked = summarize(events)
    if not result:
        return 0
    path.with_suffix(".jsonl").write_text(raw)
    stats = {k: v for k, v in result.items() if k != "result"}
    stats.update(lint_runs=ran, lint_blocked=blocked)
    path.with_suffix(".json").write_text(json.dumps(stats, indent=2))
    path.write_text(result.get("result", ""))
    print(f"   {result.get('num_turns', '?')} turns, {result.get('duration_ms', 0) / 1000:.0f}s, "
          f"${result.get('total_cost_usd', 0):.2f}, lint ran {ran}x" + (f" ({blocked} blocked)" if blocked else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
