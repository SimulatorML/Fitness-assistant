from aiogram import Router
from aiogram.types import Message
from src.dependencies import DBSession
from src.utils import get_user
from llm.workflow import process_fitness_query


router = Router()


@router.message()
async def handle_llm_query(message: Message, db_session: DBSession):
    """
    Automatically process every user message and send it to LLM.
    """
    telegram_id = message.from_user.id
    user = await get_user(telegram_id, db_session)

    if not user:
        await message.answer("Вы не зарегистрированы. Пожалуйста, используйте /start, чтобы зарегистрироваться.")
        return

    response = await process_fitness_query(message.text, telegram_id, db_session)
    
    await message.answer(response)
