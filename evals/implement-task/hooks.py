"""implement-task's own reply checks, run on every case except one with "fires": false.

The reply is either one stop line, or the five-line done report, and nothing else. The parsing is the driver's:
skills/build-phase/scripts/parse_reply.py, in strict mode.
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("parse_reply", ROOT / "skills" / "build-phase" / "scripts" / "parse_reply.py")
parse_reply = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parse_reply)


def check(reply):
    result = parse_reply.parse_implement(reply, strict=True)
    return result["problems"] if result["kind"] == "invalid" else []
