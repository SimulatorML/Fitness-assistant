import os
import yaml
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()

CONFIG_PATH = "llm/llm_config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


def get_llm():
    """Return the appropriate LLM based on the config."""
    if not os.path.isfile(CONFIG_PATH):
        raise FileNotFoundError(f"Config file llm_config.yaml not found at: {CONFIG_PATH}")
    config = load_config()
    provider = config.get("llm_provider", "openai")

    if provider == "google":
        api_key = os.getenv(config["google"]["api_key_env"])
        if not api_key:
            raise ValueError("Google API key is missing.")
        return ChatGoogleGenerativeAI(
            model=config["google"]["model"],
            google_api_key=api_key,
            temperature=0,
            convert_system_message_to_human=True
        )
    
    elif provider == "openai":
        api_key = os.getenv(config["openai"]["api_key_env"])
        if not api_key:
            raise ValueError("OpenAI API key is missing.")
        return ChatOpenAI(
            model=config["openai"]["model"],
            openai_api_key=api_key,
            temperature=0
        )

    else:
        return None
        raise ValueError(f"Unknown LLM provider: {provider}")
