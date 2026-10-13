import json
import os
from datetime import datetime
from typing import Any, Dict, List

WARNINGS_FILE = "data/warnings.json"
BLOCKED_FILE = "data/blocked_users.json"
USERS_FILE = "data/users.json"
BLACKLIST_FILE = "data/blacklist.json"


def warn_user(username: str, reason: str = "Threat detected") -> None:
    if not os.path.exists(WARNINGS_FILE):
        with open(WARNINGS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(WARNINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []

    data.append({
        "username": username,
        "reason": reason,
        "time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    })

    with open(WARNINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_warnings() -> List[Dict[str, Any]]:
    if not os.path.exists(WARNINGS_FILE):
        return []
    try:
        with open(WARNINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def get_user_warnings_count(username: str) -> int:
    warnings = get_warnings()
    count = 0
    for w in warnings:
        if isinstance(w, dict) and w.get("username") == username:
            count += 1
    return count


def block_user(username: str) -> None:
    if not os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    try:
        with open(BLOCKED_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = []

    if username not in users:
        users.append(username)

    with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def unblock_user(username: str) -> bool:
    if not os.path.exists(BLOCKED_FILE):
        return False

    try:
        with open(BLOCKED_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = []

    if username in users:
        users.remove(username)
        with open(BLOCKED_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        return True
    return False


def get_blocked_users() -> List[str]:
    if not os.path.exists(BLOCKED_FILE):
        return []
    try:
        with open(BLOCKED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def get_all_users() -> List[Dict[str, Any]]:
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except Exception:
        users = []

    blocked = set(get_blocked_users())

    try:
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
            blacklist = set(json.load(f))
    except Exception:
        blacklist = set()

    user_list = []
    for u in users:
        uname = u.get("username", "")
        role = u.get("role", "user")
        is_blocked = uname in blocked
        is_blacklisted = uname in blacklist
        warn_cnt = get_user_warnings_count(uname)

        status = "Active"
        if is_blacklisted:
            status = "Blacklisted"
        elif is_blocked:
            status = "Blocked"
        elif warn_cnt > 0:
            status = "Warned"

        user_list.append({
            "username": uname,
            "role": role,
            "status": status,
            "is_blocked": is_blocked,
            "is_blacklisted": is_blacklisted,
            "warnings_count": warn_cnt
        })

    return user_list