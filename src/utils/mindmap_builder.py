from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def _resolve_output_path(output_file: str) -> Path:
    normalized = (output_file or "").replace("\\", "/")
    target = Path(normalized)
    if target.is_absolute():
        return target
    return WORKSPACE_ROOT / target


@dataclass(frozen=True)
class MindmapLayoutConfig:
    root_x: float = 520.0
    root_y: float = 280.0
    x_gap: float = 240.0
    y_gap: float = 92.0
    min_y: float = 32.0


def build_mindmap_from_tree(
    tree: Dict[str, Any],
    config: Optional[MindmapLayoutConfig] = None,
) -> List[Dict[str, Any]]:
    """Build mindmap nodes from a tree structure."""
    cfg = config or MindmapLayoutConfig()
    normalized = _normalize_tree(tree)

    leaf_index = [0]

    def assign_y(node: Dict[str, Any]) -> float:
        children = node["children"]
        if not children:
            y = cfg.min_y + leaf_index[0] * cfg.y_gap
            leaf_index[0] += 1
            node["_y"] = y
            return y

        child_ys = [assign_y(child) for child in children]
        node["_y"] = sum(child_ys) / len(child_ys)
        return node["_y"]

    assign_y(normalized)

    root_y_shift = cfg.root_y - normalized["_y"]

    nodes: List[Dict[str, Any]] = []
    id_counter = [0]

    def next_id() -> str:
        id_counter[0] += 1
        return f"n_{id_counter[0]}"

    def walk(node: Dict[str, Any], parent_id: Optional[str], depth: int, fixed_id: Optional[str] = None) -> None:
        node_id = fixed_id or next_id()
        x = cfg.root_x + depth * cfg.x_gap
        y = node["_y"] + root_y_shift

        nodes.append(
            {
                "id": node_id,
                "text": node["title"],
                "x": round(x, 2),
                "y": round(y, 2),
                "parentId": parent_id,
            }
        )

        for child in node["children"]:
            walk(child, node_id, depth + 1)

    walk(normalized, None, 0, "root")
    return nodes


def build_mindmap_from_outline(
    outline_text: str,
    config: Optional[MindmapLayoutConfig] = None,
) -> List[Dict[str, Any]]:
    """Parse outline text and build mindmap nodes."""
    tree = _parse_outline_to_tree(outline_text)
    return build_mindmap_from_tree(tree, config=config)


def generate_mindmap_js(bot_response: str, output_file: str = "tmp/mindmap_data.js") -> List[Dict[str, Any]]:
    """Convert chatbot JSON to positioned nodes and write a data.js file.

    Supported input formats:
    1) List nodes with parent relation: [{"id", "text", "parent_id"}, ...]
    2) Dict wrapper with nodes key: {"nodes": [...]}.
    3) Already positioned list: [{"id", "text", "x", "y", "parentId"}, ...]
    """
    json_match = re.search(r"```json\s*(.*?)\s*```", bot_response, re.DOTALL)
    raw_json = json_match.group(1) if json_match else bot_response

    try:
        parsed_payload = json.loads(raw_json)
    except json.JSONDecodeError:
        print("Error: Could not parse JSON from chatbot response.")
        return []

    nodes_input: Any = parsed_payload
    if isinstance(parsed_payload, dict):
        if isinstance(parsed_payload.get("nodes"), list):
            nodes_input = parsed_payload["nodes"]
        elif isinstance(parsed_payload.get("entities"), dict) and isinstance(parsed_payload["entities"].get("nodes"), list):
            nodes_input = parsed_payload["entities"]["nodes"]

    if not isinstance(nodes_input, list):
        print("Error: Parsed payload must be a list of nodes or an object with 'nodes'.")
        return []

    root_x, root_y = 520, 280
    v_gap = 100
    h_gap = 250

    processed_nodes: List[Dict[str, Any]] = []

    # If nodes already contain absolute coordinates, keep them as-is.
    if nodes_input and all(isinstance(node, dict) and {"id", "text", "x", "y"}.issubset(node.keys()) for node in nodes_input):
        for node in nodes_input:
            parent_id = node.get("parentId")
            processed_nodes.append(
                {
                    "id": str(node.get("id")),
                    "text": str(node.get("text", "")),
                    "x": float(node.get("x")),
                    "y": float(node.get("y")),
                    "parentId": None if parent_id is None else str(parent_id),
                }
            )

        js_content = f"var externalData = {json.dumps(processed_nodes, ensure_ascii=False, indent=2)};"
        output_path = _resolve_output_path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(js_content)

        print(f"Success! Created file: {output_path}")
        return processed_nodes

    hierarchy: Dict[Optional[str], List[Dict[str, Any]]] = {}

    for node in nodes_input:
        if not isinstance(node, dict):
            continue
        parent_id = node.get("parent_id", node.get("parentId"))
        hierarchy.setdefault(parent_id, []).append(node)

    def calculate_pos(parent_id: Optional[str], start_x: float, start_y: float) -> None:
        if parent_id not in hierarchy:
            return

        children = hierarchy[parent_id]
        total_height = (len(children) - 1) * v_gap
        offset_y = start_y - (total_height / 2)

        for index, child in enumerate(children):
            curr_x = start_x + h_gap
            curr_y = offset_y + (index * v_gap)

            processed_nodes.append(
                {
                    "id": str(child["id"]),
                    "text": child["text"],
                    "x": curr_x,
                    "y": curr_y,
                    "parentId": str(parent_id),
                }
            )
            calculate_pos(child["id"], curr_x, curr_y)

    root = next(
        (
            node
            for node in nodes_input
            if isinstance(node, dict) and node.get("parent_id", node.get("parentId")) is None
        ),
        None,
    )
    if not root:
        print("Error: Could not find root node (parent_id: null)")
        return []

    processed_nodes.append(
        {
            "id": str(root["id"]),
            "text": root["text"],
            "x": root_x,
            "y": root_y,
            "parentId": None,
        }
    )

    calculate_pos(root["id"], root_x, root_y)

    js_content = f"var externalData = {json.dumps(processed_nodes, ensure_ascii=False, indent=2)};"
    output_path = _resolve_output_path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(js_content)

    print(f"Success! Created file: {output_path}")
    return processed_nodes


def _normalize_tree(tree: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(tree, dict):
        raise ValueError("tree must be a dict")

    title = str(tree.get("title", "")).strip()
    if not title:
        raise ValueError("tree.title is required")

    raw_children = tree.get("children", [])
    if raw_children is None:
        raw_children = []
    if not isinstance(raw_children, list):
        raise ValueError("tree.children must be a list")

    children = [_normalize_tree(child) for child in raw_children]
    return {"title": title, "children": children}


def _parse_outline_to_tree(outline_text: str) -> Dict[str, Any]:
    if not outline_text or not outline_text.strip():
        raise ValueError("outline_text is empty")

    lines = [line.rstrip() for line in outline_text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("outline_text is empty")

    root_title = _clean_item_text(lines[0])
    if not root_title:
        raise ValueError("Root title is empty")

    root: Dict[str, Any] = {"title": root_title, "children": []}
    stack: List[Tuple[int, Dict[str, Any]]] = [(-1, root)]

    for raw in lines[1:]:
        indent = _indent_level(raw)
        text = _clean_item_text(raw)
        if not text:
            continue

        node = {"title": text, "children": []}

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError("Invalid outline indentation")

        stack[-1][1]["children"].append(node)
        stack.append((indent, node))

    return root


def _indent_level(line: str) -> int:
    expanded = line.replace("\t", "    ")
    return len(expanded) - len(expanded.lstrip(" "))


def _clean_item_text(line: str) -> str:
    text = line.strip()
    if not text:
        return ""

    for prefix in ("- ", "* ", "+ "):
        if text.startswith(prefix):
            return text[len(prefix):].strip()

    parts = text.split(". ", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1].strip()

    return text


if __name__ == "__main__":
    sample_outline = """Chu de chinh
  - Nhanh 1
    - Chi tiet 1
  - Nhanh 2"""
    print(build_mindmap_from_outline(sample_outline))