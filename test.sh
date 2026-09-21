#!/usr/bin/env bash
# Validate every skill's structure. See tests/validate.py for the checks.
set -euo pipefail
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/tests/validate.py" "$@"
