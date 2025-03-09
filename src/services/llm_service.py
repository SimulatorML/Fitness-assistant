import logging
import aiohttp
from typing import Dict, Any
from src.config import settings

# Настроим логирование
logging.basicConfig(level=logging.INFO)

async def send_request_to_llm(
    prompt: str,
    model: str = "gemini-pro",
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """Отправляет запрос к LLM (Gemini API) и возвращает ответ."""

    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        logging.error("❌ Не найден ключ API для Gemini.")
        raise ValueError("Не найден ключ API для Gemini.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model,
        "prompt": {"text": prompt},
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(
                "https://api.generativelanguage.googleapis.com/v1beta2/models/gemini-pro:generateText",
                json=data
            ) as response:
                response.raise_for_status()
                json_response = await response.json()
                logging.info("✅ Успешный запрос к LLM")
                return json_response

    except aiohttp.ClientResponseError as e:
        logging.error(f"❌ Ошибка запроса к LLM: {e.status} {e.message}")
        raise
    except Exception as e:
        logging.error(f"❌ Неизвестная ошибка при запросе к LLM: {e}", exc_info=True)
        raise

async def process_llm_response(response: Dict[str, Any]) -> str:
    """Обрабатывает ответ от LLM (Gemini) и возвращает текстовый результат."""
    try:
        return response["candidates"][0]["output"]
    except KeyError:
        logging.error(f"❌ Ошибка обработки ответа LLM: {response}")
        return "Ошибка обработки ответа от LLM."
