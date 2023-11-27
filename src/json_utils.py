import json
from pathlib import Path


def load_json(fname: str) -> dict:
    with Path(fname).open(encoding="utf8") as f:
        return json.load(f)


def load_json_as_list(fname: str) -> list:
    return list(load_json(fname))
