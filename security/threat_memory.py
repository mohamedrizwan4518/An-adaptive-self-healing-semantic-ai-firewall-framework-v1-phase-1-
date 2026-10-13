import json
import os
from typing import List

FILE_PATH = "data/threat_memory.json"


def save_threat_pattern(pattern: str) -> None:
    if not pattern or not pattern.strip():
        return

    pattern = pattern.strip()

    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            threats: List[str] = json.load(f)
        except Exception:
            threats = []

    if pattern not in threats:
        threats.append(pattern)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(threats, f, indent=4)


def remove_threat_pattern(pattern: str) -> bool:
    if not os.path.exists(FILE_PATH):
        return False

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            threats: List[str] = json.load(f)
        except Exception:
            threats = []

    if pattern in threats:
        threats.remove(pattern)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(threats, f, indent=4)
        return True
    return False


def get_threat_patterns() -> List[str]:
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []


def clear_threat_patterns() -> None:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)