#!/usr/bin/env python3
"""Export slide and speaker-note text from PPTX files to one Markdown file.

The exporter uses only the Python standard library. It intentionally preserves
the source decks and writes a searchable AS-IS text view for archival/review.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NOTES_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"
)


def natural_key(value: str) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def paragraph_text(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []
    for paragraph in root.iter(f"{{{DRAWING_NS}}}p"):
        text = "".join(node.text or "" for node in paragraph.iter(f"{{{DRAWING_NS}}}t"))
        text = re.sub(r"\s+", " ", text).strip()
        if text and (not lines or lines[-1] != text):
            lines.append(text)
    return lines


def notes_path_for_slide(archive: zipfile.ZipFile, slide_path: str) -> str | None:
    slide = PurePosixPath(slide_path)
    rels_path = str(slide.parent / "_rels" / f"{slide.name}.rels")
    try:
        rels_root = ET.fromstring(archive.read(rels_path))
    except KeyError:
        return None

    for relationship in rels_root.findall(f"{{{REL_NS}}}Relationship"):
        if relationship.attrib.get("Type") != NOTES_REL_TYPE:
            continue
        target = relationship.attrib.get("Target")
        if not target:
            continue
        resolved = slide.parent.joinpath(target)
        normalized: list[str] = []
        for part in resolved.parts:
            if part == "..":
                if normalized:
                    normalized.pop()
            elif part != ".":
                normalized.append(part)
        return "/".join(normalized)
    return None


def deck_section(path: Path) -> tuple[int, str]:
    match = re.search(r"\]\s*(\d{2})\s+(.+)\.pptx$", path.name, re.IGNORECASE)
    if not match:
        return (999, path.stem)
    return (int(match.group(1)), match.group(2))


def markdown_escape(text: str) -> str:
    text = re.sub(
        r"(?<!\d)010[- .]?\d{3,4}[- .]?\d{4}(?!\d)",
        "[REDACTED_PHONE]",
        text,
    )
    text = re.sub(
        r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "[REDACTED_EMAIL]",
        text,
    )
    text = re.sub(
        r"(?i)(Kakao\s*ID\s*[:：]\s*)\S+",
        r"\1[REDACTED_KAKAO_ID]",
        text,
    )
    text = re.sub(
        r"https://open\.kakao\.com/o/[A-Za-z0-9]+",
        "[REDACTED_OPEN_CHAT_URL]",
        text,
    )
    return text.replace("\\", "\\\\").replace("`", "\\`")


def export_deck(path: Path) -> tuple[list[str], int, int]:
    week, title = deck_section(path)
    output = [f"## {week:02d}주차 — {title}", "", f"- 원본: `{path.name}`", ""]
    note_count = 0

    with zipfile.ZipFile(path) as archive:
        slide_paths = [
            name
            for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
        slide_paths.sort(key=natural_key)

        for slide_number, slide_path in enumerate(slide_paths, start=1):
            output.extend([f"### Slide {slide_number}", ""])
            slide_lines = paragraph_text(archive.read(slide_path))
            if slide_lines:
                output.extend(f"- {markdown_escape(line)}" for line in slide_lines)
            else:
                output.append("- _(추출 가능한 텍스트 없음: 이미지 전용 또는 빈 슬라이드)_")

            notes_path = notes_path_for_slide(archive, slide_path)
            if notes_path and notes_path in archive.namelist():
                notes_lines = paragraph_text(archive.read(notes_path))
                # PowerPoint notes placeholders often repeat the slide number alone.
                notes_lines = [
                    line
                    for line in notes_lines
                    if line not in {str(slide_number), "Click to edit Master text styles"}
                ]
                if notes_lines:
                    note_count += 1
                    output.extend(["", "#### Speaker notes", ""])
                    output.extend(f"> {markdown_escape(line)}" for line in notes_lines)
            output.append("")

    output.extend(["---", ""])
    return output, len(slide_paths), note_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    decks = sorted(args.source_dir.glob("*.pptx"), key=lambda p: deck_section(p)[0])
    if not decks:
        raise SystemExit(f"No PPTX files found in {args.source_dir}")

    body: list[str] = []
    total_slides = 0
    total_notes = 0
    per_deck: list[tuple[int, str, int, int]] = []
    for deck in decks:
        section, slide_count, note_count = export_deck(deck)
        week, title = deck_section(deck)
        body.extend(section)
        total_slides += slide_count
        total_notes += note_count
        per_deck.append((week, title, slide_count, note_count))

    generated = dt.date.today().isoformat()
    header = [
        "# AS-IS 2025년 2학기 LLMOps 슬라이드 텍스트 원문",
        "",
        (
            "> PPTX 14개에서 슬라이드 본문과 포함된 발표자 노트를 "
            "기계적으로 추출한 검색용 아카이브입니다."
        ),
        (
            "> 이미지, 도형의 의미, 애니메이션, 시각적 관계는 포함되지 않으며 "
            "문장 순서는 화면의 시각적 읽기 순서와 다를 수 있습니다."
        ),
        (
            "> 공개 Git 저장소에 불필요한 강의자 개인 연락처(전화번호·Kakao ID·이메일)는 "
            "명시적인 마스킹 토큰으로 치환했습니다. PII 교육용 가상 예시는 유지합니다."
        ),
        "",
        "## 추출 개요",
        "",
        f"- 생성일: {generated}",
        f"- 강의자료: {len(decks)}개 (01–07주차, 09–15주차)",
        "- 시험 주차: 08주차 중간고사, 16주차 팀별 프로젝트 결과 발표 — 별도 deck 없음",
        f"- 전체 슬라이드: {total_slides}장",
        f"- 발표자 노트가 추출된 슬라이드: {total_notes}장",
        "- PDF 페이지 수는 각 PPTX 슬라이드 수와 동일함",
        "",
        "| 주차 | 강의명 | 슬라이드 | 발표자 노트 |",
        "|---:|---|---:|---:|",
    ]
    header.extend(
        f"| {week:02d} | {title} | {slides} | {notes} |"
        for week, title, slides, notes in per_deck
    )
    header.extend(["", "---", ""])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(header + body), encoding="utf-8")


if __name__ == "__main__":
    main()
