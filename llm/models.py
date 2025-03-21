import os
import yaml
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from llm.config_loader import CONFIG


load_dotenv()


def get_llm():
    """Return the appropriate LLM based on the config."""
    provider = CONFIG.get("llm_provider", "openai")

    if provider == "google":
        api_key = os.getenv(CONFIG["google"]["api_key_env"])
        if not api_key:
            raise ValueError("Google API key is missing.")
        return ChatGoogleGenerativeAI(
            model=CONFIG["google"]["model"],
            google_api_key=api_key,
            temperature=0,
            convert_system_message_to_human=True
        )
    
    elif provider == "openai":
        api_key = os.getenv(CONFIG["openai"]["api_key_env"])
        if not api_key:
            raise ValueError("OpenAI API key is missing.")
        return ChatOpenAI(
            model=CONFIG["openai"]["model"],
            openai_api_key=api_key,
            temperature=0
        )

    else:
        return None #TODO: remove in production
        raise ValueError(f"Unknown LLM provider: {provider}")
