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
from src.database.connection import session_maker
from src.utils import get_user


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
    Handle the "start" command and start the onboarding process if user not found in database.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
        db_session (Session): The database session.
    """
    await state.clear()
    user = await get_user(message.from_user.id, db_session)
    if user:
        # TODO: Rework welcome message
        await message.answer(
            text=f'С возвращением, {user.name}! Чем хотите заняться?'
        )
    else:
        await message.answer(
            text='Добро пожаловать! Этот бот помогает достигать лучших '
                'результатов в физической активности с помощью ИИ.\n\n\n'
                'Для продолжения необходимо заполнить небольшую анкету о себе!\n'
                'Пожалуйста, введите Ваше имя:'
        )
        await state.set_state(FSMFillForm.name)


@dp.message(Command("updateprofile"))
async def update_profile(message: Message, db_session: Session):
    """
    Handle the "updateprofile" command and update the user profile.
    
    Args:
        message (Message): The message sent by the user.
        db_session (Session): The database session.
    """
    user = await get_user(message.from_user.id, db_session)
    if user:
        # TODO: Add update logic
        await message.answer("Профиль обновлен!")
    else:
        await message.answer("Профиль не найден. Пожалуйста выполните команду /start, чтобы заполните профиль.")


@dp.message(Command("profileinfo"))
async def show_profile_info(message: Message, db_session: Session):
    """
    Handle the "profileinfo" command and show the user profile info.
    
    Args:
        message (Message): The message sent by the user.
        db_session (Session): The database session.
    """
    user = await get_user(message.from_user.id, db_session)
    if user:
        await message.answer(f"""Информация о профиле:
        Имя: {user.name}
        Дата рождения: {user.birth_date}
        Пол: {user.gender}
        Рост: {user.height}
        Вес: {user.weight}
        Уровень активности: {user.activity_level}
        Цель: {user.goal}
        Ограничения здоровья: {user.health_restrictions}
        Предпочтения по активностям: {user.preferred_activities}""")
    else:
        await message.answer("Профиль не найден. Пожалуйста выполните команду /start, чтобы заполните профиль.")


@dp.message(Command("getrecommendation"))
async def process_get_recommendations_command(message: Message, db_session: Session):
    user = await get_user(message.from_user.id, db_session)
    if user:
        await message.answer("Рекомендация")
    else:
        await message.answer("Профиль не найден. Пожалуйста выполните команду /start, чтобы заполните профиль.")


@dp.message(Command("addactivity"))
async def process_add_activity_command(message: Message, db_session: Session):
    """
    Handle the "addactivity" command and add the user's activity to the profile.
    
    Args:
        message (Message): The message sent by the user.
        db_session (Session): The database session.
    """
    user = await get_user(message.from_user.id, db_session)
    if user:
        # TODO: Add adding activity logic
        await message.answer("Активность добавлена!")
    else:
        await message.answer("Профиль не найден. Пожалуйста выполните команду /start, чтобы заполните профиль.")


@dp.message(Command("help"))
async def process_help_command(message: Message):
    # TODO: Add help message
    await message.answer("Помощь")


@dp.message(Command("deleteprofile")) # For testing, maybe will be removed
async def process_delete_profile_command(message: Message, db_session: Session):
    user = await get_user(message.from_user.id, db_session)
    await db_session.delete(user)
    await db_session.commit()
    await message.answer("Профиль удален!")


register_onboarding_handlers(dp)


if __name__ == '__main__':
    dp.run_polling(bot)
