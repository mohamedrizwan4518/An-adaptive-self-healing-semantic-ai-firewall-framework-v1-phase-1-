import json
from collections import Counter
from typing import Any, Dict, List


def generate_threat_intelligence() -> Dict[str, Any]:


    try:
        with open("data/attacks.json", "r", encoding="utf-8") as f:
            attacks: List[Dict[str, Any]] = json.load(f)
    except Exception:

        attacks = []

        return {

            "total_attacks": 0,

            "most_common_attack": "None",

            "most_targeted_user": "None",

            "highest_risk_user": "None",

            "attack_distribution": {}

        }

    total_attacks = len(attacks)

    attack_types: List[str] = []

    users: List[str] = []

    for attack in attacks:

        attack_types.append(

            attack.get(
                "type",
                "Unknown"
            )

        )

        users.append(

            attack.get(
                "username",
                "Unknown"
            )

        )

    attack_counter: Any = Counter(attack_types)

    user_counter: Any = Counter(users)

    most_common_attack: str = (
        attack_counter.most_common(1)[0][0] if attack_counter else "None"
    )

    most_targeted_user: str = (
        user_counter.most_common(1)[0][0] if user_counter else "None"
    )

    highest_risk_user: str = (
        user_counter.most_common(1)[0][0] if user_counter else "None"
    )

    return {

        "total_attacks":
        total_attacks,

        "most_common_attack":
        most_common_attack,

        "most_targeted_user":
        most_targeted_user,

        "highest_risk_user":
        highest_risk_user,

        "attack_distribution":
        dict(
            attack_counter
        )

    }