#!/usr/bin/env bash
# Validate every skill's structure (tests/validate.py), then run the unit tests (tests/test_*.py).
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$root/tests/validate.py" "$@"
python3 -m unittest discover -s "$root/tests" -p 'test_*.py'
