"""Extract later-year required occurrences of matrix courses from 2025+ DX tables."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


ROOT = Path(__file__).resolve().parents[1]
SOURCE = next((ROOT / "src").glob("★2026학년도 교육과정 운영기준 및 편성표*.docx"))

DEPARTMENTS = [
    "건축공학전공", "토목공학전공", "산업공학전공", "수리빅데이터전공",
    "고분자공학전공", "신소재공학전공", "소재디자인공학전공",
    "화학공학전공", "화학생명소재전공",
]

COURSES = [
    "글쓰기와발표", "글로벌커뮤니케이션", "디지털문해력", "대학수학1", "대학수학2",
    "일반물리학1", "일반물리학2", "일반화학1", "일반화학2",
    "일반물리학실험1", "일반물리학실험2", "일반화학실험1", "일반화학실험2",
    "창의입문설계", "컴퓨터프로그래밍언어", "확률및통계",
    "건축토목환경공학개론", "스마트그린빌딩의이해", "건축과컴퓨터",
    "공업역학", "스마트제조개론", "빅데이터의세계",
]


def compact(text: str) -> str:
    return "".join(text.replace("*", "").split())


def blocks(parent: _Document):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def table_rows(table: Table):
    return [[" ".join(cell.text.split()) for cell in row.cells] for row in table.rows]


def parse_course_rows(rows):
    results = []
    if not rows:
        return results
    cols = len(rows[0])
    if cols == 9:
        layouts = [(1, 2, 3, 1), (5, 6, 7, 2)]  # type, code, name, semester
    elif cols == 8:
        layouts = [(1, 2, 3, 1), (1, 5, 6, 2)]
    else:
        return results

    for row_index, row in enumerate(rows[1:], start=1):
        if len(row) != cols:
            continue
        year_text = compact(row[0])
        if not year_text or not year_text[0].isdigit():
            continue
        year = int(year_text[0])
        for type_col, code_col, name_col, semester in layouts:
            normalized_name = compact(row[name_col])
            for course in COURSES:
                if normalized_name == compact(course):
                    course_type = compact(row[type_col])
                    results.append({
                        "course": course,
                        "year": year,
                        "semester": semester,
                        "type": row[type_col],
                        "code": row[code_col],
                        "required": "필" in course_type,
                        "row_index": row_index,
                    })
    return results


def main():
    doc = Document(SOURCE)
    current_department = ""
    recent = deque(maxlen=10)
    table_index = -1
    selected = {}

    for block in blocks(doc):
        if isinstance(block, Paragraph):
            text = " ".join(block.text.split())
            if text:
                recent.append(text)
                for department in DEPARTMENTS:
                    if department in text:
                        current_department = department
            continue

        table_index += 1
        rows = table_rows(block)
        joined = compact(" ".join(cell for row in rows for cell in row))
        # 2025+ department-specific liberal/MSC tables always contain these three codes/names.
        if (
            current_department in DEPARTMENTS
            and current_department not in selected
            and all(token in joined for token in ("디지털문해력", "대학수학1", "글쓰기"))
        ):
            occurrences = parse_course_rows(rows)
            if occurrences:
                selected[current_department] = {
                    "table_index": table_index,
                    "context": list(recent),
                    "rows": rows,
                    "occurrences": occurrences,
                }

    summary = {
        department: {
            "table_index": payload["table_index"],
            "occurrences": payload["occurrences"],
        }
        for department, payload in selected.items()
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
