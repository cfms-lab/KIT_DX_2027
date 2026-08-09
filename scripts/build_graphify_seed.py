"""Create a deterministic Graphify extraction seed from the SQLite dataset."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "data" / "dx_curriculum.sqlite"
OUTPUT = ROOT / "graphify-out" / ".graphify_seed.json"


def course_id(name: str) -> str:
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:12]
    return f"data_course_{digest}"


def base_node(node_id: str, label: str, file_type: str, source_file: Path, source_location: str) -> dict[str, object]:
    return {
        "id": node_id,
        "label": label,
        "file_type": file_type,
        "source_file": str(source_file.resolve()),
        "source_location": source_location,
        "source_url": None,
        "captured_at": None,
        "author": None,
        "contributor": None,
    }


def main() -> None:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    hyperedges: list[dict[str, object]] = []

    department_nodes: dict[str, str] = {}
    for row in connection.execute("SELECT * FROM departments ORDER BY department_id"):
        node_id = f"data_department_{row['department_id'].lower()}"
        department_nodes[row["department_id"]] = node_id
        node = base_node(
            node_id,
            row["department_name"],
            "document",
            ROOT / "data" / "departments.csv",
            f"department_id={row['department_id']}",
        )
        node["entity_type"] = "department"
        node["is_engineering_accredited"] = bool(row["is_engineering_accredited"])
        nodes.append(node)

    course_rows = connection.execute(
        """
        SELECT course_name_canonical,
               GROUP_CONCAT(DISTINCT course_code) AS course_codes,
               COUNT(DISTINCT department_id) AS department_count
        FROM course_offerings
        GROUP BY course_name_canonical
        ORDER BY course_name_canonical
        """
    ).fetchall()
    course_nodes: dict[str, str] = {}
    for row in course_rows:
        name = row["course_name_canonical"]
        node_id = course_id(name)
        course_nodes[name] = node_id
        node = base_node(
            node_id,
            name,
            "concept",
            ROOT / "data" / "course_offerings.csv",
            f"course_name_canonical={name}",
        )
        node["entity_type"] = "course"
        node["course_codes"] = row["course_codes"]
        node["department_count"] = row["department_count"]
        nodes.append(node)

    summary_concepts = (
        (
            "data_concept_first_year_common",
            "1학년 9개 전공 공통 필수과목",
            """
            SELECT course_name_canonical
            FROM course_offerings
            WHERE year = 1 AND is_effectively_required = 1
            GROUP BY course_name_canonical
            HAVING COUNT(DISTINCT department_id) = 9
            """,
            ROOT / "data" / "course_overlap.csv",
        ),
        (
            "data_concept_later_msc_overlap",
            "2~4학년 공통 MSC 필수과목",
            "SELECT course_name_canonical FROM v_later_msc_required_overlap",
            ROOT / "data" / "course_overlap.csv",
        ),
    )
    for concept_id, concept_label, query, source_file in summary_concepts:
        concept = base_node(concept_id, concept_label, "rationale", source_file, concept_label)
        concept["entity_type"] = "summary_concept"
        nodes.append(concept)
        for row in connection.execute(query):
            name = row[0]
            if name not in course_nodes:
                continue
            edges.append({
                "source": concept_id,
                "target": course_nodes[name],
                "relation": "references",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "source_file": str(source_file.resolve()),
                "source_location": name,
                "weight": 2.0,
            })

    offerings = connection.execute(
        """
        SELECT department_id, department_name, course_name_canonical,
               GROUP_CONCAT(DISTINCT course_code) AS course_codes,
               GROUP_CONCAT(DISTINCT year || '-' || semester) AS year_terms,
               GROUP_CONCAT(DISTINCT curriculum_area) AS curriculum_areas,
               MAX(is_msc) AS is_msc,
               MAX(is_design_course) AS is_design_course,
               MAX(is_curriculum_required) AS is_curriculum_required,
               MAX(is_policy_required) AS is_policy_required,
               MAX(is_effectively_required) AS is_effectively_required
        FROM course_offerings
        GROUP BY department_id, course_name_canonical
        ORDER BY department_id, course_name_canonical
        """
    ).fetchall()
    for row in offerings:
        relation = "implements" if row["is_effectively_required"] else "references"
        edges.append({
            "source": department_nodes[row["department_id"]],
            "target": course_nodes[row["course_name_canonical"]],
            "relation": relation,
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
            "source_file": str((ROOT / "data" / "course_offerings.csv").resolve()),
            "source_location": f"{row['department_name']} | {row['course_name_canonical']} | {row['year_terms']}",
            "weight": 2.0 if row["is_effectively_required"] else 1.0,
            "year_terms": row["year_terms"],
            "course_codes": row["course_codes"],
            "curriculum_areas": row["curriculum_areas"],
            "is_msc": bool(row["is_msc"]),
            "is_design_course": bool(row["is_design_course"]),
            "is_curriculum_required": bool(row["is_curriculum_required"]),
            "is_policy_required": bool(row["is_policy_required"]),
            "is_effectively_required": bool(row["is_effectively_required"]),
        })

    overlaps = connection.execute(
        """
        SELECT course_name_canonical
        FROM course_overlap
        WHERE department_count_effective_required >= 2
        ORDER BY course_name_canonical
        """
    ).fetchall()
    for row in overlaps:
        name = row["course_name_canonical"]
        department_ids = [
            department_nodes[item[0]]
            for item in connection.execute(
                """
                SELECT DISTINCT department_id
                FROM course_offerings
                WHERE course_name_canonical = ? AND is_effectively_required = 1
                ORDER BY department_id
                """,
                (name,),
            )
        ]
        if len(department_ids) >= 2:
            hyperedges.append({
                "id": f"overlap_{course_id(name).removeprefix('data_course_')}",
                "label": f"{name} 공통 필수 전공군",
                "nodes": department_ids + [course_nodes[name]],
                "relation": "participate_in",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "source_file": str((ROOT / "data" / "course_overlap.csv").resolve()),
            })

    connection.close()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(
            {
                "nodes": nodes,
                "edges": edges,
                "hyperedges": hyperedges,
                "input_tokens": 0,
                "output_tokens": 0,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"seed_nodes={len(nodes)} seed_edges={len(edges)} seed_hyperedges={len(hyperedges)}")


if __name__ == "__main__":
    main()
