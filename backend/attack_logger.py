import json
import os
from datetime import datetime
from typing import Any, Dict, List, Union


def log_attack(
    username: str,
    attack_text: str,
    attack_type: str,
    category: str,
    score: Union[int, float],
    reason: str,
    risk: str = "High",
) -> None:
 
 try:

    attack: Dict[str, Any] = {

        "username": username,

        "attack": attack_text,

        "type": attack_type,

        "category": category,

        "risk": risk,

        "score": score,

        "reason": reason,

        "time": str(datetime.now())

    }

    project_root = os.path.abspath(

        os.path.join(

            os.path.dirname(__file__),

            ".."

        )

    )

    file_path = os.path.join(

        project_root,

        "data",

        "attacks.json"

    )

    os.makedirs(

        os.path.dirname(file_path),

        exist_ok=True

    )

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data: List[Dict[str, Any]] = json.load(f)
        except Exception:
            data = []

    data.append(attack)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"ATTACK SAVED: {category}"
    )

 except Exception as e:

    print(
        f"LOGGER ERROR: {str(e)}"
    )

