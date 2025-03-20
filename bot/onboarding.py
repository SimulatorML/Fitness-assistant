from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext
from src.database.models import User, Action
from src.schemas.action import ActionType
from sqlalchemy.orm import Session
from src.utils import calculate_age


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


async def process_name_sent(message: Message, state: FSMContext):
    """
    Handle the name sent by the user and ask for the birth date.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
    """
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите Вашу дату рождения в формате ГГГГ-ММ-ДД:')
    await state.set_state(FSMFillForm.birth_date)


async def process_birth_date(message: Message, state: FSMContext):
    """
    Handle the birth date sent by the user and ask for the gender.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
    """
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

    # Create inline keyboard buttons
    male_button = InlineKeyboardButton(
        text='Мужской ♂',
        callback_data='male'
    )
    female_button = InlineKeyboardButton(
        text='Женский ♀',
        callback_data='female'
    )
    # Add buttons to keyboard
    keyboard: list[list[InlineKeyboardButton]] = [
        [male_button, female_button]
        ]
    # Create inline keyboard object
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Send message with inline keyboard
    await message.answer(
        text='Спасибо!\n\nУкажите Ваш пол',
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.gender)

async def process_gender(callback: CallbackQuery, state: FSMContext):
    """
    Handle the gender sent by the user and ask for the height.
    
    Args:
        callback (CallbackQuery): The callback query sent by the user.
        state (FSMContext): The state machine context.
    """
    await state.update_data(gender=callback.data)
    await callback.message.answer(
        text='Спасибо! А теперь введите Ваш рост:'
    )
    await state.set_state(FSMFillForm.height)

async def process_height(message: Message, state: FSMContext):
    """
    Handle the height sent by the user and ask for the weight.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
    """
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

async def process_weight(message: Message, state: FSMContext):
    """
    Handle the weight sent by the user and ask for the activity level.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
    """
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
        text='Лёгкая активность (1-2 раза в неделю, прогулки)',
        callback_data='light'
    )
    moderate_button = InlineKeyboardButton(
        text='Умеренная активность (тренировки 3-4 раза в неделю)',
        callback_data='moderate'
    )
    high_button = InlineKeyboardButton(
            text='Высокая активность (тренировки 5+ раз в неделю)',
            callback_data='high'
    )
    athlete_button = InlineKeyboardButton(
            text='Профессиональный уровень (спортсмен, тренировки 2 раза в день)',
            callback_data='athlete'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [sedentary_button],
        [light_button],
        [moderate_button],
        [high_button],
        [athlete_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer("Выберите Ваш уровень активности", reply_markup=markup)
    await state.set_state(FSMFillForm.activity_level)

async def process_activity_level(callback: CallbackQuery, state: FSMContext):
    """
    Handle the activity level sent by the user and ask for the goal.
    
    Args:
        callback (CallbackQuery): The callback query sent by the user.
        state (FSMContext): The state machine context.
    """
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
        [fat_loss_button],
        [muscle_gain_button],
        [maintenance_button],
        [endurance_button],
        [strength_button],
        [flexibility_button],
        [health_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback.message.answer("Какая Ваша цель?", reply_markup=markup)
    await state.set_state(FSMFillForm.goal)

async def process_goal(callback: CallbackQuery, state: FSMContext):
    """
    Handle the goal sent by the user and ask for the health restrictions.
    
    Args:
        callback (CallbackQuery): The callback query sent by the user.
        state (FSMContext): The state machine context.
    """
    await state.update_data(goal=callback.data)
    await callback.message.answer("Напишите в вольной форме, есть ли у Вас какие-либо заболевания, травмы и т.д. (если нет - поставьте прочерк \"-\"):")
    await state.set_state(FSMFillForm.health_restrictions)

async def process_health_restrictions(message: Message, state: FSMContext):
    """
    Handle the health restrictions sent by the user and ask for the preferred activities.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
    """
    await state.update_data(health_restrictions=message.text)
    await message.answer("Есть ли у Вас какие-либо предпочтения по активностям (например каждую неделю плаваете, ходите в спортзал и т.д.)? Если нет - поставьте прочерк \"-\"")
    await state.set_state(FSMFillForm.preferred_activities)

async def process_preferred_activities(message: Message, state: FSMContext, db_session: Session):
    """
    Handle the preferred activities sent by the user and save the user data to the database.
    
    Args:
        message (Message): The message sent by the user.
        state (FSMContext): The state machine context.
        db_session (Session): The database session.
    """
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

def register_onboarding_handlers(dp: Dispatcher):
    """
    Register onboarding handlers for telegram bot.
    
    Args:
        dp: Dispatcher
    """
    dp.message.register(process_name_sent, FSMFillForm.name)
    dp.message.register(process_birth_date, FSMFillForm.birth_date)
    dp.callback_query.register(process_gender, FSMFillForm.gender)
    dp.message.register(process_height, FSMFillForm.height)
    dp.message.register(process_weight, FSMFillForm.weight)
    dp.callback_query.register(process_activity_level, FSMFillForm.activity_level)
    dp.callback_query.register(process_goal, FSMFillForm.goal)
    dp.message.register(process_health_restrictions, FSMFillForm.health_restrictions)
    dp.message.register(process_preferred_activities, FSMFillForm.preferred_activities)
