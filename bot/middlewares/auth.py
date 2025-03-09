import logging

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext  # If you need to interact with the state
from typing import Callable, Dict, Any, Awaitable
from bot.utils.api_client import FitnessAPIClient

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        api_client = FitnessAPIClient()
        user_id = event.from_user.id
        try:
            user = await api_client.get_user(user_id)
            if user:
                data['user'] = user
                return await handler(event, data)
            else:
                if isinstance(event, Message):
                    await event.answer("Пожалуйста, создайте профиль с помощью /profile.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("Пожалуйста, создайте профиль с помощью /profile.")
        except Exception as e:
            logger.exception(f"Error in AuthMiddleware: {e}")
            if isinstance(event, Message):
                await event.answer("Произошла ошибка. Попробуйте позже.")
            elif isinstance(event, CallbackQuery):
                await event.answer("Произошла ошибка. Попробуйте позже.")