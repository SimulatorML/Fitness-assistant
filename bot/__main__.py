from dotenv import load_dotenv
import os
from typing import Callable, Dict, Any, Awaitable
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, TelegramObject
from sqlalchemy.orm import sessionmaker, Session
from bot.onboarding import register_onboarding_handlers
from src.database.models import User
from sqlalchemy import select
from src.database.connection import session_maker


load_dotenv()

class DBSessionMiddleware(BaseMiddleware):
    """
    Middleware that provides the database session to the handler.
    """
    def __init__(self, session_maker: sessionmaker) -> None:
        super().__init__()
        self.session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if "db_session" in data.get("handler").params:
            async with self.session_maker() as session:
                data["db_session"] = session
                return await handler(event, data)
        return await handler(event, data)


bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db_session_middleware = DBSessionMiddleware(session_maker=session_maker)
dp.message.middleware(db_session_middleware)
dp.callback_query.middleware(db_session_middleware)


class FSMFillForm(StatesGroup):
    name = State()
    birth_date = State()
    gender = State()
    height = State()
    weight = State()
    activity_level = State()
    goal = State()
    health_restrictions = State()
    preferred_activities = State()


@dp.message(CommandStart(), StateFilter('*'))
async def process_start_command(message: Message, state: FSMContext, db_session: Session):
    """
    Handle the start command and start the onboarding process if user not found in database.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
        db_session (Session): The database session.
    """
    await state.clear()
    telegram_id = message.from_user.id
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        await message.answer(
            text='Добро пожаловать! Этот бот помогает достигать лучших '
                'результатов в физической активности с помощью ИИ.\n\n\n'
                'Для продолжения необходимо заполнить небольшую анкету о себе!\n'
                'Пожалуйста, введите Ваше имя:'
        )
        await state.set_state(FSMFillForm.name)
    else:
        await message.answer(
            text=f'С возвращением, {user.name}! Чем хотите заняться?'
        )

@dp.message(Command("updateprofile"))
async def update_profile(message: Message, state: FSMContext):
    await message.answer("Профиль обновлен!")

@dp.message(Command("help"))
async def process_help_command(message: Message):
    await message.answer("Помощь")

@dp.message(Command("getrecommendations"))
async def process_get_recommendations_command(message: Message):
    await message.answer("Рекомендации")


register_onboarding_handlers(dp)


if __name__ == '__main__':
    dp.run_polling(bot)
