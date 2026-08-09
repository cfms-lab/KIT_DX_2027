"""Map relevant source tables to DX department sections using coded headings."""

from __future__ import annotations

import argparse
import re
from collections import deque
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

from extract_dx_2025_required import COURSES, DEPARTMENTS, compact


ROOT = Path(__file__).resolve().parents[1]
SOURCE = next((ROOT / "src").glob("★2026학년도 교육과정 운영기준 및 편성표*.docx"))


def blocks(parent: _Document):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--department", choices=DEPARTMENTS)
    args = parser.parse_args()
    doc = Document(SOURCE)
    recent = deque(maxlen=8)
    current_target = ""
    table_index = -1

    for block in blocks(doc):
        if isinstance(block, Paragraph):
            text = " ".join(block.text.split())
            if text:
                recent.append(text)
            # A five-digit curriculum code marks the start of a department/program section.
            if re.search(r"\(\d{5}\)", text):
                current_target = next((d for d in DEPARTMENTS if d in text), "")
            continue

        table_index += 1
        if not current_target or (args.department and current_target != args.department):
            continue
        rows = [[" ".join(c.text.split()) for c in row.cells] for row in block.rows]
        joined = compact(" ".join(c for row in rows for c in row))
        hits = [course for course in COURSES if compact(course) in joined]
        if not hits:
            continue
        print(
            f"DEPT={current_target} TABLE={table_index} ROWS={len(rows)} COLS={len(rows[0]) if rows else 0} "
            f"HITS={','.join(hits)}"
        )
        print("CTX=" + " || ".join(recent))
        for row in rows[:4]:
            print("  " + " | ".join(row))


if __name__ == "__main__":
    main()
