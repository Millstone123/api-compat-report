from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def load_json(path: str | Path) -> Any:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_shape_errors(value: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(value, dict):
        return ["schema must be a JSON object"]
    if value.get("type") != "object":
        errors.append("schema type must be object")
    properties = value.get("properties")
    if not isinstance(properties, dict):
        errors.append("schema properties must be an object")
        return errors
    for name, definition in properties.items():
        if not isinstance(name, str) or not isinstance(definition, dict):
            errors.append("property definitions must be objects")
            continue
        if "type" not in definition:
            errors.append("property %s is missing type" % name)
        if "enum" in definition and not isinstance(definition["enum"], list):
            errors.append("property %s enum must be a list" % name)
    required = value.get("required", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        errors.append("required must be a list of property names")
    return errors


def sample_shape_errors(value: Any) -> List[str]:
    if not isinstance(value, dict):
        return ["sample must be a JSON object"]
    if not isinstance(value.get("fixture"), str):
        return ["sample fixture must be a string"]
    if not isinstance(value.get("data"), dict):
        return ["sample data must be an object"]
    return []


def structural_check(schema: Any, sample: Any = None) -> Tuple[List[str], List[str]]:
    return schema_shape_errors(schema), sample_shape_errors(sample) if sample is not None else []
