from __future__ import annotations

import importlib
from typing import Any, Callable, Dict, List


MODULES = {"compatibility": "api_compatibility.conflict"}


def load_resolver(selector: str) -> Callable[..., Dict[str, Any]]:
    module = importlib.import_module(MODULES[selector])
    return module.resolve


def resolve_conflicts(before: Dict[str, Any], after: Dict[str, Any], changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    selector = after.get("x-resolution", "compatibility")
    return load_resolver(selector)(before, after, changes)
