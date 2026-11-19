"""Records when the tests last ran, for the editor's status bar."""

import time
from pathlib import Path

(Path(__file__).resolve().parents[1] / ".last-test-run").write_text(f"{time.time()}\n")
