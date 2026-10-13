import json
from typing import Any, Dict, List


def login(username: str, password: str) -> Dict[str, Any]:
    with open("data/users.json", "r") as f:
        users: List[Dict[str, Any]] = json.load(f)

    for user in users:
        if user.get("username") == username and user.get("password") == password:
            return {"success": True, "role": user.get("role", "user")}

    return {"success": False}