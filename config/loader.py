import os
import json

CONFIG_DIR = os.path.dirname(__file__)

def load(*names):
    """
    Load configuration from multiple JSON files.
    If no names are provided, it defaults to loading 'config.json'\
    If a file is not found, it raises a FileNotFoundError.
    """

    config = {}
    for name in names:
        path = os.path.join(CONFIG_DIR, f"{name}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            config.update(data)
    return config
 