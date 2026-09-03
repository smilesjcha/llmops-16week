#!/usr/bin/env python3
"""Sort `## NN주차` Markdown sections while preserving header and footer."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

WEEK_HEADING = re.compile(r"^##\s+(\d{2})주차\b.*$", re.MULTILINE)
FOOTER_HEADING = re.compile(r"^##\s+공통\s+수업\s+운영\s+체크리스트\b", re.MULTILINE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    matches = list(WEEK_HEADING.finditer(text))
    if not matches:
        raise SystemExit("No weekly sections found")

    footer_match = FOOTER_HEADING.search(text)
    footer_start = footer_match.start() if footer_match else len(text)
    header = text[: matches[0].start()].rstrip()
    footer = text[footer_start:].lstrip() if footer_match else ""

    sections: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else footer_start
        end = min(next_start, footer_start)
        if match.start() >= footer_start:
            continue
        sections.append((int(match.group(1)), text[match.start() : end].strip()))

    weeks = [week for week, _ in sections]
    if len(weeks) != len(set(weeks)):
        raise SystemExit(f"Duplicate weekly headings: {weeks}")

    parts = [header, *[section for _, section in sorted(sections)], footer]
    output = "\n\n".join(part for part in parts if part).rstrip() + "\n"
    args.path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
