"""Merge deterministic curriculum seed and semantic Graphify chunks."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphify-out"


def normalized_label(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def main() -> None:
    inputs = [OUT / ".graphify_seed.json"]
    if (OUT / ".graphify_cached.json").exists():
        inputs.append(OUT / ".graphify_cached.json")
    inputs += sorted(OUT.glob(".graphify_chunk_*.json"))
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in inputs]
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    hyperedges: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    label_to_id: dict[str, str] = {}
    id_remap: dict[str, str] = {}

    for payload in payloads:
        for node in payload.get("nodes", []):
            node_id = str(node["id"])
            label_key = normalized_label(str(node.get("label", "")))
            existing = label_to_id.get(label_key)
            if existing:
                id_remap[node_id] = existing
                continue
            if node_id in seen_ids:
                raise ValueError(f"Duplicate node ID with different label: {node_id}")
            seen_ids.add(node_id)
            label_to_id[label_key] = node_id
            id_remap[node_id] = node_id
            nodes.append(node)

    edge_by_pair: dict[tuple[str, str], int] = {}
    for payload in payloads:
        for edge in payload.get("edges", []):
            updated = dict(edge)
            updated["source"] = id_remap.get(str(edge["source"]), str(edge["source"]))
            updated["target"] = id_remap.get(str(edge["target"]), str(edge["target"]))
            if updated["source"] == updated["target"]:
                continue
            pair = tuple(sorted((str(updated["source"]), str(updated["target"]))))
            existing_index = edge_by_pair.get(pair)
            if existing_index is not None:
                existing = edges[existing_index]
                # The final graph is undirected and simple. Prefer the exact
                # SQLite-backed required relationship over a generic semantic
                # reference when both describe the same endpoints.
                if existing.get("relation") != "implements" and updated.get("relation") == "implements":
                    edges[existing_index] = updated
                continue
            edge_by_pair[pair] = len(edges)
            edges.append(updated)

    hyperedge_keys: set[tuple[str, ...]] = set()
    for payload in payloads:
        for hyperedge in payload.get("hyperedges", []):
            updated = dict(hyperedge)
            members = []
            for member in hyperedge.get("nodes", []):
                mapped = id_remap.get(str(member), str(member))
                if mapped not in members:
                    members.append(mapped)
            if len(members) < 3:
                continue
            updated["nodes"] = members
            key = tuple(sorted(members))
            if key in hyperedge_keys:
                continue
            hyperedge_keys.add(key)
            hyperedges.append(updated)

    semantic = {
        "nodes": nodes,
        "edges": edges,
        "hyperedges": hyperedges,
        "input_tokens": 0,
        "output_tokens": 0,
    }
    (OUT / ".graphify_semantic_new.json").write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / ".graphify_semantic.json").write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    ast_path = OUT / ".graphify_ast.json"
    ast = (
        json.loads(ast_path.read_text(encoding="utf-8"))
        if ast_path.exists()
        else {"nodes": [], "edges": []}
    )
    extraction = {
        "nodes": ast.get("nodes", []) + nodes,
        "edges": ast.get("edges", []) + edges,
        "hyperedges": hyperedges,
        "input_tokens": 0,
        "output_tokens": 0,
    }
    (OUT / ".graphify_extract.json").write_text(
        json.dumps(extraction, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"merged_nodes={len(nodes)} merged_edges={len(edges)} merged_hyperedges={len(hyperedges)}")


if __name__ == "__main__":
    main()
