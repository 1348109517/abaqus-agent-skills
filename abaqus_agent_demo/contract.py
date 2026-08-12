import hashlib
import json
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    pass


def load_contract(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load contract {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("contract must be a top-level JSON object")
    return value


def input_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
