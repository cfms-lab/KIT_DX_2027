"""Inspect source DOCX tables for target-course occurrences by DX department."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


DEPARTMENTS = [
    "건축공학전공", "토목공학전공", "산업공학전공", "수리빅데이터전공",
    "고분자공학전공", "신소재공학전공", "소재디자인공학전공",
    "화학공학전공", "화학생명소재전공",
]

COURSES = [
    "글쓰기와발표", "글로벌커뮤니케이션", "디지털문해력", "대학수학1", "대학수학2",
    "일반물리학1", "일반물리학2", "일반화학1", "일반화학2",
    "일반물리학실험1", "일반물리학실험2", "일반물리학실험",
    "일반화학실험1", "일반화학실험2", "창의입문설계",
    "컴퓨터프로그래밍언어", "확률및통계", "확률", "통계", "프로그래밍", "건축토목환경공학개론",
    "스마트그린빌딩의이해", "건축과컴퓨터", "공업역학", "스마트제조개론", "빅데이터의세계",
]


def compact(text: str) -> str:
    return " ".join(text.split())


def blocks(parent: _Document):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()

    doc = Document(args.docx)
    recent = deque(maxlen=10)
    current_department = ""
    table_index = -1

    for block in blocks(doc):
        if isinstance(block, Paragraph):
            text = compact(block.text)
            if text:
                recent.append(text)
                for department in DEPARTMENTS:
                    if department in text:
                        current_department = department
            continue

        table_index += 1
        rows = [[compact(cell.text) for cell in row.cells] for row in block.rows]
        joined = " | ".join(cell for row in rows for cell in row)
        for department in DEPARTMENTS:
            if department in joined:
                current_department = department

        hits = []
        for row_index, row in enumerate(rows):
            row_text = " | ".join(row)
            course_hits = [course for course in COURSES if course in row_text]
            if course_hits:
                hits.append((row_index, course_hits, row))

        if hits and current_department in DEPARTMENTS:
            print(f"\nDEPT={current_department} TABLE={table_index} ROWS={len(rows)} COLS={len(rows[0]) if rows else 0}")
            print("CONTEXT=" + " || ".join(recent))
            for row_index, course_hits, row in hits:
                print(f"ROW={row_index} HIT={','.join(course_hits)} :: " + " | ".join(row))


if __name__ == "__main__":
    main()
