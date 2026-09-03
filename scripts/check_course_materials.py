#!/usr/bin/env python3
"""Offline structural checks for all preserved course notebooks."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRACTICE = ROOT / "AS-IS 2025 2nd semester" / "practice"
EXPECTED_NOTEBOOKS = 16
AUTHORED_NOTEBOOKS = [ROOT / "week01" / "lab" / "week01_trace01_lab.ipynb"]
SHELL_OR_MAGIC = re.compile(r"^\s*(?:!|%|pip\s+install\b)")


def sanitize_cell(source: str) -> str:
    """Remove notebook-only shell/magic lines before Python syntax checks."""
    return "\n".join(
        line for line in source.splitlines() if not SHELL_OR_MAGIC.match(line)
    )


def main() -> int:
    notebooks = sorted(PRACTICE.rglob("*.ipynb"))
    errors: list[str] = []
    syntax_warnings: list[str] = []

    if len(notebooks) != EXPECTED_NOTEBOOKS:
        errors.append(f"expected {EXPECTED_NOTEBOOKS} notebooks, found {len(notebooks)}")

    for path in notebooks:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
            continue

        if data.get("nbformat") != 4:
            errors.append(f"{path.relative_to(ROOT)}: nbformat is not 4")

        language = data.get("metadata", {}).get("language_info", {}).get("name")
        if language not in {None, "python"}:
            errors.append(f"{path.relative_to(ROOT)}: unexpected language {language!r}")

        for index, cell in enumerate(data.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            source = sanitize_cell("".join(cell.get("source", [])))
            if not source.strip():
                continue
            try:
                ast.parse(source)
            except SyntaxError as exc:
                syntax_warnings.append(
                    f"{path.relative_to(ROOT)} cell {index}: {exc.msg} at line {exc.lineno}"
                )

    for path in AUTHORED_NOTEBOOKS:
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing authored notebook")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
            continue

        if data.get("nbformat") != 4:
            errors.append(f"{path.relative_to(ROOT)}: nbformat is not 4")

        for index, cell in enumerate(data.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            source = sanitize_cell("".join(cell.get("source", [])))
            if not source.strip():
                continue
            try:
                ast.parse(source)
            except SyntaxError as exc:
                errors.append(
                    f"{path.relative_to(ROOT)} cell {index}: {exc.msg} at line {exc.lineno}"
                )

    print(
        f"preserved_notebooks={len(notebooks)} authored_notebooks={len(AUTHORED_NOTEBOOKS)} "
        f"structural_errors={len(errors)} "
        f"syntax_warnings={len(syntax_warnings)}"
    )
    for warning in syntax_warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
