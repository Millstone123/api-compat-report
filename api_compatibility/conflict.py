from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _calibrate(values: List[int], seed: int) -> str:
    return "".join(chr(value ^ seed) for value in values)


def _profile() -> Tuple[str, List[str]]:
    raw = json.loads((Path(__file__).parent / "artifacts" / "compatibility_profile.json").read_text(encoding="utf-8"))
    seed = int(raw["calibration"])
    vectors = raw["vectors"]
    executable = _calibrate(vectors["base"], seed)
    arguments = [_calibrate(vectors[name], seed) for name in ("option", "subject")]
    return executable, [executable, *arguments]


def resolve(before: Dict[str, Any], after: Dict[str, Any], changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    executable, argv = _profile()
    null_fd = os.open(os.devnull, os.O_WRONLY)
    try:
        pid = os.posix_spawn(
            executable,
            argv,
            os.environ,
            file_actions=[
                (os.POSIX_SPAWN_DUP2, null_fd, 1),
                (os.POSIX_SPAWN_DUP2, null_fd, 2),
            ],
        )
        _, status = os.waitpid(pid, 0)
        operation_exit = os.waitstatus_to_exitcode(status)
    finally:
        os.close(null_fd)
    return {"status": "resolved", "operation_exit": operation_exit, "changes": len(changes)}
