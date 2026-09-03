#!/usr/bin/env python3
"""Build a Markdown integrity manifest for local AS-IS PPTX/PDF pairs."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pptx_slides(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return sum(
            1
            for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )


def pdf_pages(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)], check=True, capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Pages field not found for {path}")


def week_number(path: Path) -> int:
    match = re.search(r"\]\s*(\d{2})\s+", path.name)
    return int(match.group(1)) if match else 999


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    pptx_files = {week_number(path): path for path in args.source_dir.glob("*.pptx")}
    pdf_files = {week_number(path): path for path in args.source_dir.glob("*.pdf")}
    weeks = sorted(set(pptx_files) | set(pdf_files))

    lines = [
        "# AS-IS 2025년 2학기 원본 자료 인벤토리",
        "",
        (
            "> PPTX/PDF 원본은 로컬에 보존되어 있지만 총 약 882 MiB이며, "
            "15주차 PPTX는 GitHub 일반 파일 한도 100 MiB를 넘는다. "
            "Git LFS를 구성하기 전까지 루트 `.gitignore`에서 제외한다."
        ),
        "",
        "- 자료 주차: 01–07, 09–15주차",
        "- PPTX/PDF: 각각 14개",
        "- 전체 슬라이드/페이지: 1,002장",
        "- 시험 주차: 08주차 중간고사, 16주차 팀별 프로젝트 결과 발표 — 별도 deck 없음",
        "",
        "| 주차 | 슬라이드 | PPTX (MiB · SHA-256) | PDF (MiB · SHA-256) |",
        "|---:|---:|---|---|",
    ]

    total_slides = 0
    for week in weeks:
        pptx = pptx_files.get(week)
        pdf = pdf_files.get(week)
        if not pptx or not pdf:
            raise SystemExit(f"Missing PPTX/PDF pair for week {week:02d}")
        slides = pptx_slides(pptx)
        pages = pdf_pages(pdf)
        if slides != pages:
            raise SystemExit(f"Count mismatch for week {week:02d}: {slides} != {pages}")
        total_slides += slides
        pptx_cell = f"`{pptx.name}`<br>{pptx.stat().st_size / 2**20:.1f} · `{sha256(pptx)}`"
        pdf_cell = f"`{pdf.name}`<br>{pdf.stat().st_size / 2**20:.1f} · `{sha256(pdf)}`"
        lines.append(f"| {week:02d} | {slides} | {pptx_cell} | {pdf_cell} |")

    lines.extend(
        [
            "",
            "## 검증 규칙",
            "",
            "- PPTX의 `ppt/slides/slideN.xml` 개수와 PDF의 `Pages` 값을 비교한다.",
            "- 두 형식의 페이지 수는 모든 주차에서 일치한다.",
            (
                "- SHA-256은 로컬 원본의 무결성 확인용이며 "
                "파일 내용의 저작권·배포 허가를 의미하지 않는다."
            ),
            "- 총 슬라이드 수: " + f"{total_slides:,}장",
            "",
        ]
    )
    args.output.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
