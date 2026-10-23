import json
import os


def load_config(config_path="config/config.json"):
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            "Copy config/config.example.json to config/config.json and fill in your tokens."
        )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_token(config, key, env_var=None):
    """Get token from config or environment variable."""
    if env_var and os.environ.get(env_var):
        return os.environ[env_var]
    return config.get(key, "")
