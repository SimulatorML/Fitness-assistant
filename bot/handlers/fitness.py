import logging
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot.states.user_states import UserForm
from bot.keyboards.inline import (gender_keyboard, activity_level_keyboard,
                                    goal_keyboard, confirm_keyboard, health_restrictions_keyboard, activities_keyboard)
from bot.utils.api_client import FitnessAPIClient
from datetime import datetime

router = Router()
api_client = FitnessAPIClient()

# --- Вспомогательные функции ---
async def format_profile_text(user_data: dict) -> str:
    """Формирует текст профиля пользователя."""
    activities = user_data.get('preferred_activities', [])
    activities_str = ', '.join(activities) if activities else "Не указано"

    profile_text = (
        "📋 Ваш профиль:\n\n"
        f"👤 Имя: {user_data.get('name', 'Не указано')}\n"
        f"🎂 Дата рождения: {user_data.get('birth_date', 'Не указано')}\n"
        f"🧍‍♂️ Пол: {user_data.get('gender', 'Не указано')}\n"
        f"📏 Рост: {user_data.get('height', 'Не указано')} см\n"
        f"⚖️ Вес: {user_data.get('weight', 'Не указано')} кг\n"
        f"🤸 Уровень активности: {user_data.get('activity_level', 'Не указано')}\n"
        f"🎯 Цель: {user_data.get('goal', 'Не указано')}\n"
        f"🩺 Ограничения: {user_data.get('health_restrictions', 'Не указано')}\n"
        f"🏃 Активности: {activities_str}\n"
    )
    return profile_text

# --- Начало онбординга (/profile) ---
@router.message(Command("profile"), StateFilter(None))
async def cmd_profile(message: Message, state: FSMContext):
    await message.answer('📝 Давайте создадим ваш фитнес-профиль!\nКак вас зовут?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserForm.name)

# --- Обработка имени ---
@router.message(StateFilter(UserForm.name), F.text.isalpha())
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Приятно познакомиться, {message.text}!\n'
                            f'Введите дату рождения в формате ДД.ММ.ГГГГ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserForm.birth_date)

@router.message(StateFilter(UserForm.name))
async def process_name_invalid(message: Message):
    await message.answer("Пожалуйста, введите имя, используя только буквы.")

# --- Обработка даты рождения ---
@router.message(StateFilter(UserForm.birth_date))
async def process_birth_date(message: Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text, '%d.%m.%Y')
        if date_obj > datetime.now():
            raise ValueError
        await state.update_data(birth_date=message.text)
        await message.answer("Выберите ваш пол:", reply_markup=gender_keyboard())
        await state.set_state(UserForm.gender)
    except ValueError:
        await message.answer('❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ')

# --- Обработка пола ---
@router.callback_query(StateFilter(UserForm.gender))
async def process_gender(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback_query.data)
    await callback_query.message.edit_text('Введите ваш рост в см (например, 175)')
    await state.set_state(UserForm.height)
    await callback_query.answer()

# --- Обработка роста ---
@router.message(StateFilter(UserForm.height), F.text.isdigit(), lambda message: 100 <= int(message.text) <= 250)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer('Введите ваш вес в кг (например, 70)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserForm.weight)

@router.message(StateFilter(UserForm.height))
async def process_height_invalid(message: Message):
    await message.answer('Введите ваш рост в см (от 100 до 250)')

# --- Обработка веса ---
@router.message(StateFilter(UserForm.weight), F.text.isdigit(), lambda message: 30 <= int(message.text) <= 300)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer('Выберите уровень активности:', reply_markup=activity_level_keyboard())
    await state.set_state(UserForm.activity_level)

@router.message(StateFilter(UserForm.weight))
async def process_weight_invalid(message: Message):
    await message.answer('Введите ваш вес в кг (от 30 до 300)')

# --- Обработка уровня активности ---
@router.callback_query(StateFilter(UserForm.activity_level))
async def process_activity_level(callback_query: CallbackQuery, state: FSMContext):
    activity_map = {'beginner': 'Начинающий', 'intermediate': 'Средний', 'advanced': 'Продвинутый'}
    await state.update_data(activity_level=activity_map.get(callback_query.data))
    await callback_query.message.edit_text('🎯 Выберите вашу цель:', reply_markup=goal_keyboard())
    await state.set_state(UserForm.goal)
    await callback_query.answer()

# --- Обработка цели ---
@router.callback_query(StateFilter(UserForm.goal))
async def process_goal(callback_query: CallbackQuery, state: FSMContext):
    goal_map = {'weight_loss': 'Похудение', 'muscle_gain': 'Набор массы', 'maintenance': 'Поддержание формы'}
    await state.update_data(goal=goal_map.get(callback_query.data))
    await callback_query.message.edit_text('Есть ли у вас ограничения по здоровью?', reply_markup=health_restrictions_keyboard())
    await state.set_state(UserForm.health_restrictions)
    await callback_query.answer()

# --- Обработка ограничений по здоровью (выбор) ---
@router.callback_query(StateFilter(UserForm.health_restrictions))
async def process_restrictions_choice(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'has_restrictions':
        await callback_query.message.edit_text('Опишите ваши ограничения:')
        await state.set_state(UserForm.health_restrictions)
    else:
        await state.update_data(health_restrictions='Нет')
        await show_activities_selection(callback_query.message, state)
    await callback_query.answer()

# --- Обработка ограничений по здоровью (текст) ---
@router.message(StateFilter(UserForm.health_restrictions), F.text)
async def process_restrictions_text(message: Message, state: FSMContext):
    await state.update_data(health_restrictions=message.text)
    await show_activities_selection(message, state)

@router.message(StateFilter(UserForm.health_restrictions))
async def process_restrictions_text_invalid(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите текстом")

# --- Показ выбора активностей ---
async def show_activities_selection(message: Message, state: FSMContext):
    await message.answer('🏃 Выберите предпочитаемые активности:', reply_markup=activities_keyboard())
    await state.set_state(UserForm.select_activities)

# --- Обработка выбора активностей ---
@router.callback_query(StateFilter(UserForm.select_activities))
async def process_activity(callback_query: CallbackQuery, state: FSMContext):
    # Здесь реализуйте логику обработки выбора активностей
    await callback_query.message.answer("Вы выбрали активности")
    await state.finish()  # или установите новое состояние, если нужно
    await callback_query.answer()