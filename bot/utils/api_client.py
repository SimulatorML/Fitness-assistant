import httpx
import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")
logger = logging.getLogger(__name__)

class FitnessAPIClient:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url

    async def __aenter__(self):
        """Запускает `AsyncClient` в контексте `async with`"""
        self.client = httpx.AsyncClient(base_url=self.base_url)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Гарантированно закрывает `AsyncClient` после использования."""
        await self.client.aclose()

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.post("/users/", json=user_data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error creating user: {e.response.status_code} - {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"Request error creating user: {e}")
                raise

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.get(f"/users/{user_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.info(f"User {user_id} not found.")
                    return None
                logger.error(f"Error getting user: {e.response.status_code} - {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"Request error getting user: {e}")
                raise
   
    async def delete_user(self, user_id: int) -> None:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.delete(f"/users/{user_id}")
                response.raise_for_status()
                logger.info(f"✅ User {user_id} deleted successfully.")
            except httpx.HTTPStatusError as e:
                logger.error(f"❌ Error deleting user: {e.response.status_code} - {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"❌ Request error deleting user: {e}")
                raise
