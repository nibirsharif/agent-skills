"""Fails when a function in textstats/ raises an exception that its docstring does not name."""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def problems(path):
    for node in ast.walk(ast.parse(path.read_text())):
        if not isinstance(node, ast.FunctionDef):
            continue
        doc = ast.get_docstring(node) or ""
        for inner in ast.walk(node):
            if not isinstance(inner, ast.Raise) or inner.exc is None:
                continue
            raised = inner.exc.func if isinstance(inner.exc, ast.Call) else inner.exc
            name = getattr(raised, "id", None)
            if name and name not in doc:
                where = f"{path.relative_to(ROOT)}:{inner.lineno}"
                yield f"{where}: {node.name} raises {name}, which its docstring does not name"


def main():
    found = [p for path in sorted((ROOT / "textstats").glob("*.py")) for p in problems(path)]
    print("\n".join(found) if found else "docstrings OK")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
