import json
import os
from typing import List

FILE = "data/blacklist.json"


def blacklist_user(username: str) -> None:
    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            users: List[str] = json.load(f)
    except Exception:
        users = []

    if username not in users:
        users.append(username)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def remove_blacklist(username: str) -> bool:
    if not os.path.exists(FILE):
        return False

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            users: List[str] = json.load(f)
    except Exception:
        users = []

    if username in users:
        users.remove(username)
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        return True
    return False


def get_blacklist() -> List[str]:
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []