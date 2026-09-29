from __future__ import annotations

from typing import Any, Dict, List


def render_report(result: Dict[str, Any], before_name: str, after_name: str) -> str:
    lines = ["# API compatibility report", "", "Compared `%s` with `%s`." % (before_name, after_name), "", "## Changes", ""]
    changes: List[Dict[str, Any]] = result.get("changes", [])
    if not changes:
        lines.append("No schema changes detected.")
    for item in changes:
        lines.append("- `%s`: %s%s" % (item["property"], item["kind"], " (breaking)" if item["breaking"] else ""))
    lines.extend(["", "## Result", "", "Compatible: %s" % ("no" if any(item["breaking"] for item in changes) else "yes")])
    return "\n".join(lines) + "\n"
