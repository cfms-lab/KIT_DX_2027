"""Small command-line query helper for the generated curriculum database."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "data" / "dx_curriculum.sqlite"


def print_rows(rows: list[sqlite3.Row]) -> None:
    if not rows:
        print("No rows found.")
        return
    headers = rows[0].keys()
    widths = {
        header: max(len(str(header)), *(len(str(row[header] if row[header] is not None else "")) for row in rows))
        for header in headers
    }
    print(" | ".join(str(header).ljust(widths[header]) for header in headers))
    print("-+-".join("-" * widths[header] for header in headers))
    for row in rows:
        print(" | ".join(str(row[header] if row[header] is not None else "").ljust(widths[header]) for header in headers))


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--course", help="정규화 과목명 일부 검색")
    group.add_argument("--department", help="전공명 일부 검색")
    group.add_argument("--later-msc-overlap", action="store_true")
    args = parser.parse_args()

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    if args.course:
        rows = connection.execute(
            """
            SELECT department_name, year_label, semester, curriculum_area,
                   requirement_type_raw, course_code, course_name_raw,
                   course_name_canonical, is_effectively_required, required_reason
            FROM course_offerings
            WHERE course_name_canonical LIKE ?
            ORDER BY course_name_canonical, department_name, year, semester
            """,
            (f"%{args.course.replace(' ', '')}%",),
        ).fetchall()
    elif args.department:
        rows = connection.execute(
            """
            SELECT department_name, year_label, semester, curriculum_area,
                   requirement_type_raw, course_code, course_name_canonical, credits
            FROM course_offerings
            WHERE department_name LIKE ?
            ORDER BY year, semester, course_code
            """,
            (f"%{args.department}%",),
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT course_name_canonical, department_count, departments, year_terms
            FROM v_later_msc_required_overlap
            ORDER BY department_count DESC, course_name_canonical
            """
        ).fetchall()
    print_rows(list(rows))
    connection.close()


if __name__ == "__main__":
    main()
