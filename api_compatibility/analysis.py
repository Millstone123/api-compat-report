from __future__ import annotations

from typing import Any, Dict, List

from .dispatch import resolve_conflicts
from .schema import load_json, structural_check


def _property_changes(before: Dict[str, Any], after: Dict[str, Any]) -> List[Dict[str, Any]]:
    old = before.get("properties", {})
    new = after.get("properties", {})
    changes: List[Dict[str, Any]] = []
    for name in sorted(set(old) | set(new)):
        if name not in old:
            changes.append({"property": name, "kind": "added", "breaking": False})
        elif name not in new:
            changes.append({"property": name, "kind": "removed", "breaking": True})
        elif old[name] != new[name]:
            breaking = old[name].get("type") != new[name].get("type")
            changes.append({"property": name, "kind": "changed", "breaking": breaking})
    old_required = set(before.get("required", []))
    new_required = set(after.get("required", []))
    for name in sorted(new_required - old_required):
        changes.append({"property": name, "kind": "required", "breaking": True})
    return changes


def _sample_violations(schema: Dict[str, Any], sample: Dict[str, Any]) -> List[str]:
    data = sample.get("data", {})
    violations: List[str] = []
    required = set(schema.get("required", []))
    for name in sorted(required - set(data)):
        violations.append("missing required property: %s" % name)
    properties = schema.get("properties", {})
    for name in sorted(set(data) & set(properties)):
        expected = properties[name].get("type")
        actual = type(data[name]).__name__
        type_names = {"str": "string", "int": "integer", "float": "number", "bool": "boolean", "dict": "object", "list": "array", "NoneType": "null"}
        if expected and type_names.get(actual, actual) != expected:
            violations.append("property %s expects %s" % (name, expected))
        enum = properties[name].get("enum")
        if isinstance(enum, list) and data[name] not in enum:
            violations.append("property %s is outside enum" % name)
    return violations


def compare_documents(before_path: str, after_path: str, resolve: bool = True) -> Dict[str, Any]:
    before = load_json(before_path)
    after = load_json(after_path)
    errors = structural_check(before)[0] + structural_check(after)[0]
    if errors:
        return {"valid": False, "errors": errors, "changes": []}
    changes = _property_changes(before, after)
    result = {"valid": True, "errors": [], "changes": changes}
    if resolve and any(item["breaking"] for item in changes):
        result["resolution"] = resolve_conflicts(before, after, changes)
    return result


def review_document(path: str) -> Dict[str, Any]:
    value = load_json(path)
    errors = structural_check(value)[0]
    return {"valid": not errors, "errors": errors, "properties": sorted(value.get("properties", {})) if not errors else []}


def validate_sample(sample_path: str, schema_path: str, resolve: bool = True) -> Dict[str, Any]:
    sample = load_json(sample_path)
    schema = load_json(schema_path)
    errors = structural_check(schema, sample)[0] + structural_check(schema, sample)[1]
    if errors:
        return {"valid": False, "errors": errors}
    violations = _sample_violations(schema, sample)
    result = {"valid": not violations, "errors": violations}
    if resolve and not violations:
        result["resolution"] = resolve_conflicts(schema, schema, [{"property": sample.get("fixture"), "kind": "validated", "breaking": False}])
    return result
