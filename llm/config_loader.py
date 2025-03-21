from dotenv import load_dotenv
import os
from pathlib import Path
import yaml

load_dotenv()

CONFIG_PATH = Path(os.environ.get("LLM_CONFIG_PATH", "llm/llm_config.yaml"))

if not CONFIG_PATH.is_file():
    raise FileNotFoundError(f"Config not found at {CONFIG_PATH.resolve()}")


def load_config():
    with CONFIG_PATH.open("r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()