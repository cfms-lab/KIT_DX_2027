"""Verify the generated DX curriculum CSV and SQLite artifacts."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


EXPECTED_LATER_MSC = {
    "확률및통계": {"건축공학전공", "토목공학전공", "소재디자인공학전공"},
    "공학수학": {"건축공학전공", "토목공학전공", "산업공학전공"},
    "고급프로그래밍언어": {"산업공학전공", "수리빅데이터전공", "소재디자인공학전공"},
    "공학수학1": {"고분자공학전공", "신소재공학전공", "화학공학전공"},
    "공학수학2": {"고분자공학전공", "신소재공학전공", "화학공학전공"},
}


def main() -> None:
    with (DATA / "course_offerings.csv").open(encoding="utf-8-sig", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    connection = sqlite3.connect(DATA / "dx_curriculum.sqlite")
    connection.row_factory = sqlite3.Row

    assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert connection.execute("SELECT COUNT(*) FROM departments").fetchone()[0] == 9
    assert connection.execute("SELECT COUNT(*) FROM course_offerings").fetchone()[0] == len(csv_rows)

    common = connection.execute(
        """
        SELECT course_name_canonical
        FROM course_offerings
        WHERE year = 1 AND is_effectively_required = 1
        GROUP BY course_name_canonical
        HAVING COUNT(DISTINCT department_id) = 9
        ORDER BY course_name_canonical
        """
    ).fetchall()
    common_names = {row[0] for row in common}
    assert {"글쓰기와발표", "글로벌커뮤니케이션", "디지털문해력", "대학수학1", "대학수학2"} <= common_names

    later_rows = connection.execute(
        """
        SELECT course_name_canonical, department_name
        FROM course_offerings
        WHERE is_msc = 1 AND is_effectively_required = 1 AND year BETWEEN 2 AND 4
        """
    ).fetchall()
    actual: dict[str, set[str]] = {}
    for row in later_rows:
        actual.setdefault(row[0], set()).add(row[1])
    for course, departments in EXPECTED_LATER_MSC.items():
        assert actual.get(course) == departments, (course, actual.get(course), departments)

    design_rows = connection.execute(
        """
        SELECT department_name, is_curriculum_required, is_policy_required, is_effectively_required
        FROM course_offerings
        WHERE course_name_canonical = '창의입문설계'
        ORDER BY department_name
        """
    ).fetchall()
    assert len(design_rows) == 5
    chem_bio = next(row for row in design_rows if row[0] == "화학생명소재전공")
    assert tuple(chem_bio[1:]) == (0, 0, 0)
    accredited = [row for row in design_rows if row[0] != "화학생명소재전공"]
    assert all(row[2] == 1 and row[3] == 1 for row in accredited)

    connection.close()
    print(f"PASS: 9 departments, {len(csv_rows)} offerings, SQLite/CSV consistent")
    print("PASS: first-year 9-department common courses verified")
    print("PASS: five later-year MSC overlap groups verified")
    print("PASS: engineering-accreditation design policy markers verified")


if __name__ == "__main__":
    main()
