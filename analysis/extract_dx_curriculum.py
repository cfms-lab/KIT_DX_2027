"""Inspect and extract first-year curriculum tables from the 2026 DOCX source."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


TARGETS = (
    "건축공학전공",
    "토목공학전공",
    "산업공학전공",
    "수리빅데이터전공",
    "고분자공학전공",
    "신소재공학전공",
    "소재디자인공학전공",
    "화학공학전공",
    "화학생명소재전공",
)


def iter_blocks(parent: _Document):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def compact(text: str) -> str:
    return " ".join(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--ranges", default="60-85,105-125,220-260,265-320,450-530")
    parser.add_argument("--year-tables-only", action="store_true")
    args = parser.parse_args()

    selected: set[int] = set()
    for item in args.ranges.split(","):
        start, end = (int(value) for value in item.split("-", 1))
        selected.update(range(start, end + 1))

    doc = Document(args.docx)
    recent = deque(maxlen=6)
    table_index = -1

    for block in iter_blocks(doc):
        if isinstance(block, Paragraph):
            text = compact(block.text)
            if text:
                recent.append(text)
            continue

        table_index += 1
        if table_index not in selected:
            continue

        cells = [compact(cell.text) for row in block.rows for cell in row.cells]
        joined = " | ".join(cells)
        row0 = " | ".join(compact(cell.text) for cell in block.rows[0].cells) if block.rows else ""
        if args.year_tables_only and not row0.startswith(("학년", "이수 학년")):
            continue
        target_hits = [name for name in TARGETS if name in joined or any(name in p for p in recent)]
        print(f"\nTABLE {table_index} rows={len(block.rows)} cols={len(block.columns)} targets={','.join(target_hits)}")
        print("CONTEXT:", " || ".join(recent))
        print("ROW0:", row0[:700])


if __name__ == "__main__":
    main()
