from datetime import datetime
from dotenv import load_dotenv
import os
from typing import Callable, Dict, Any, Awaitable
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, TelegramObject)
from sqlalchemy.orm import sessionmaker, Session
from src.database.models import User, Action
from src.schemas.action import ActionType
from sqlalchemy import select
from src.database.connection import session_maker


load_dotenv()

class DBSessionMiddleware(BaseMiddleware):
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


# Этот хэндлер будет срабатывать на команду /start вне состояний
# переводит бота в состояние ожидания ввода имени если новый пользователь
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext, db_session: Session):
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


# переводит в состояние ожидания ввода даты рождения
@dp.message(StateFilter(FSMFillForm.name))
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите Вашу дату рождения в формате ГГГГ-ММ-ДД:')
    await state.set_state(FSMFillForm.birth_date)


def calculate_age(birth_date: datetime) -> int:
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# переводит в состояние выбора пола
@dp.message(StateFilter(FSMFillForm.birth_date))
async def process_age(message: Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%Y-%m-%d")
    except ValueError:
        await message.answer("Некорректный формат даты. Введите в формате ГГГГ-ММ-ДД:")
        return

    age = calculate_age(birth_date)
    if not (16 <= age <= 90):
        await message.answer("Возраст должен быть от 16 до 90 лет. Пожалуйста, проверьте дату рождения и введите еще раз в формате ГГГГ-ММ-ДД:")
        return
    await state.update_data(birth_date=birth_date)

    # Создаем объекты инлайн-кнопок
    male_button = InlineKeyboardButton(
        text='Мужской ♂',
        callback_data='male'
    )
    female_button = InlineKeyboardButton(
        text='Женский ♀',
        callback_data='female'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [male_button, female_button]
        ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Спасибо!\n\nУкажите Ваш пол',
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.gender)


# переводит в состояние ввода роста
@dp.callback_query(StateFilter(FSMFillForm.gender))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    # await callback.message.delete() # нужно ли нам удалять сообщение с кнопками????
    await callback.message.answer(
        text='Спасибо! А теперь введите Ваш рост:'
    )
    # Устанавливаем состояние ожидания ввода роста
    await state.set_state(FSMFillForm.height)


# Обработчик для ввода роста с проверкой диапазона
@dp.message(FSMFillForm.height)
async def process_height(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число для роста.")
        return
    height = int(message.text)
    if not (100 <= height <= 250):
        await message.answer("Рост должен быть в диапазоне от 100 до 250 см. Попробуйте еще раз:")
        return
    await state.update_data(height=height)
    await message.answer("Теперь введите ваш вес (в кг):")
    await state.set_state(FSMFillForm.weight)


# Обработчик для ввода веса с проверкой диапазона
@dp.message(FSMFillForm.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = message.text.replace(',', '.')
        weight = float(weight)
        if not (30 <= weight <= 160):
            raise ValueError
    except ValueError:
        await message.answer("Вес должен быть в диапазоне от 30 до 160 кг. Например: 56.7, 89,5.\nПопробуйте еще раз:")
        return
    await state.update_data(weight=round(weight, 1))

    # Create ActivityLevel buttons (src/schemas/user.py)
    sedentary_button = InlineKeyboardButton(
        text='Малоподвижный образ жизни',
        callback_data='sedentary'
    )
    light_button = InlineKeyboardButton(
        text='Лёгкая активность (какая-либо активность 1-2 раза в неделю, прогулки)',
        callback_data='light'
    )
    moderate_button = InlineKeyboardButton(
        text='Умеренная активность (тренировки 3-4 раза в неделю)',
        callback_data='moderate'
    )
    high_button = InlineKeyboardButton(
            text='Высокая активность (интенсивные тренировки 5+ раз в неделю)',
            callback_data='high'
    )
    athlete_button = InlineKeyboardButton(
            text='Профессиональный уровень (спортсмен, тренировки 2 раза в день)',
            callback_data='athlete'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [sedentary_button, light_button],
        [moderate_button, high_button],
        [athlete_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer("Выберите Ваш уровень активности", reply_markup=markup)
    await state.set_state(FSMFillForm.activity_level)


@dp.callback_query(FSMFillForm.activity_level)
async def process_activity_level(callback: CallbackQuery, state: FSMContext):
    await state.update_data(activity_level=callback.data)

    # Create Goal buttons (src/schemas/user.py)
    fat_loss_button = InlineKeyboardButton(
        text='Сжигание жира',
        callback_data='fat_loss'
    )
    muscle_gain_button = InlineKeyboardButton(
        text='Набор мышечной массы',
        callback_data='muscle_gain'
    )
    maintenance_button = InlineKeyboardButton(
        text='Поддержание формы',
        callback_data='maintenance'
    )
    endurance_button = InlineKeyboardButton(
            text='Развитие выносливости',
            callback_data='endurance'
    )
    strength_button = InlineKeyboardButton(
            text='Увеличение силы',
            callback_data='strength'
    )
    flexibility_button = InlineKeyboardButton(
            text='Улучшение гибкости',
            callback_data='flexibility'
    )
    health_button = InlineKeyboardButton(
            text='Общее улучшение здоровья',
            callback_data='health'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [fat_loss_button, muscle_gain_button],
        [maintenance_button, endurance_button],
        [strength_button, flexibility_button],
        [health_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.answer("Какая Ваша цель?", reply_markup=markup)
    await state.set_state(FSMFillForm.goal)


@dp.callback_query(FSMFillForm.goal)
async def process_activity_level(callback: CallbackQuery, state: FSMContext):
    await state.update_data(goal=callback.data)
    await callback.message.answer("Напишите в вольной форме, есть ли у Вас какие-либо заболевания, травмы и т.д.:")
    await state.set_state(FSMFillForm.health_restrictions)


@dp.message(FSMFillForm.health_restrictions)
async def process_activity_level(message: Message, state: FSMContext):
    await state.update_data(health_restrictions=message.text)
    await message.answer("Есть ли у Вас какие-либо предпочтения по активностям (например каждую неделю плаваете, ходите в спортзал и т.д.)?")
    await state.set_state(FSMFillForm.preferred_activities)


@dp.message(FSMFillForm.preferred_activities)
async def process_activity_level(message: Message, state: FSMContext, db_session: Session):
    await state.update_data(preferred_activities=message.text)
    data = await state.get_data()
    data["telegram_id"] = message.from_user.id
    new_user = User(**data)
    db_session.add(new_user)
    await db_session.flush()
    await db_session.refresh(new_user)
    action = Action(time=new_user.created_at, user_id=new_user.id, action_type=ActionType.REGISTRATION)
    db_session.add(action)
    await db_session.commit()
    await message.answer("Отлично! Теперь, мы можем сможем давать Вам персонализированные рекомендации!\nЕсли что-то поменяется (вес, цели) - Вы можете изменить это в любое время")
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)
