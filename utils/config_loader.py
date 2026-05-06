"""utils/config_loader.py — Load and validate config.json"""

import json
import sys


REQUIRED_KEYS = [
    "sender_email",
    "sender_password",
    "sender_name",
]


def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"\n  [!] Config file not found: {path}")
        print("      Copy config.example.json → config.json and fill in your details.\n")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n  [!] config.json has invalid JSON: {e}\n")
        sys.exit(1)

    # Strip internal/comment keys (any key starting with "_")
    config = {k: v for k, v in raw.items() if not k.startswith("_")}

    missing = [k for k in REQUIRED_KEYS if not config.get(k)]
    if missing:
        print(f"\n  [!] Missing required fields in config.json: {missing}\n")
        sys.exit(1)

    return config
