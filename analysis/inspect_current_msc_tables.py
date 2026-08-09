"""Print the current-curriculum MSC/basic-science tables for the nine DX majors."""

from __future__ import annotations

from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
SOURCE = next((ROOT / "src").glob("★2026학년도 교육과정 운영기준 및 편성표*.docx"))

TABLES = {
    "건축공학전공": [73],
    "토목공학전공": [113],
    "산업공학전공": [228],
    "수리빅데이터전공": [253],
    "고분자공학전공": [271],
    "신소재공학전공": [291, 292],
    "소재디자인공학전공": [459, 460],
    "화학공학전공": [492, 493],
    "화학생명소재전공": [517, 518],
}


def main() -> None:
    doc = Document(SOURCE)
    for department, indices in TABLES.items():
        print(f"\n===== {department} =====")
        for index in indices:
            table = doc.tables[index]
            print(f"--- TABLE {index}: {len(table.rows)} rows x {len(table.columns)} cols ---")
            for row_number, row in enumerate(table.rows):
                cells = [" ".join(cell.text.split()) for cell in row.cells]
                print(f"{row_number:02d}: " + " | ".join(cells))


if __name__ == "__main__":
    main()
