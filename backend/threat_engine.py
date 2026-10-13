import json
from typing import Literal


def calculate_user_score(username: str) -> int:
    score = 0

    try:
        with open("data/attacks.json", "r", encoding="utf-8") as f:
            attacks = json.load(f)
        for attack in attacks:
            if attack.get("username") == username:
                score += 20
    except Exception:
        pass

    try:
        with open("data/warnings.json", "r", encoding="utf-8") as f:
            warnings = json.load(f)
        for w in warnings:
            if isinstance(w, dict) and w.get("username") == username:
                score += 10
    except Exception:
        pass

    try:
        with open("data/blocked_users.json", "r", encoding="utf-8") as f:
            blocked = json.load(f)
        if username in blocked:
            score = max(score, 85)
    except Exception:
        pass

    try:
        with open("data/blacklist.json", "r", encoding="utf-8") as f:
            blacklist = json.load(f)
        if username in blacklist:
            score = 100
    except Exception:
        pass

    return min(score, 100)


def get_risk_level(score: int) -> Literal["Low", "Medium", "High"]:
    if score < 30:
        return "Low"
    elif score < 70:
        return "Medium"
    return "High"