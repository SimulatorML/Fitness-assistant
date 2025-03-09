from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot.states.user_states import FSMFitnessProfile  # Предполагается, что FSMFitnessProfile определён в этом модуле
from bot.keyboards.inline import (
    gender_keyboard,
    activity_level_keyboard,
    goal_keyboard,
    confirm_keyboard,
    health_restrictions_keyboard,
    activities_keyboard
)
from bot.utils.api_client import FitnessAPIClient
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

router = Router()
api_client = FitnessAPIClient()

# Глобальный словарь для хранения данных профиля (если нужен, либо используйте БД)
user_dict = {}

# Хэндлер на /start
@router.message(CommandStart(), StateFilter())
async def process_start_command(message: Message):
    await message.answer(
        text='Добро пожаловать в фитнес-бот!\n\n'
             'Для заполнения профиля отправьте команду /profile'
    )

# Хэндлер на /cancel вне состояний
@router.message(Command("cancel"), StateFilter())
async def process_cancel_command(message: Message, state: FSMContext):
    # Если пользователь вне профиля, можно вернуть стандартное сообщение
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            text='Отмена невозможна. Вы вне профиля.\n\n'
                 'Для заполнения профиля отправьте команду /profile'
        )
    else:
        await state.clear()
        await message.answer(
            text='Заполнение профиля отменено.\n\n'
                 'Для повторного заполнения отправьте команду /profile'
        )

# Хэндлер на /profile
@router.message(Command("profile"), StateFilter())
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Введите ваше имя:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFitnessProfile.fill_name)

# Обработка имени
@router.message(StateFilter(FSMFitnessProfile.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Отлично! Теперь введите ваш возраст:')
    await state.set_state(FSMFitnessProfile.fill_age)

# Предупреждение при неправильном вводе имени
@router.message(StateFilter(FSMFitnessProfile.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='Это не похоже на имя. Пожалуйста, введите ваше имя.\n\n'
             'Для отмены отправьте /cancel'
    )

# Обработка возраста
@router.message(StateFilter(FSMFitnessProfile.fill_age), lambda m: m.text.isdigit() and 4 <= int(m.text) <= 120)
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    # Создаем inline кнопки для выбора пола
    male_button = InlineKeyboardButton(text='Мужской ♂', callback_data='male')
    female_button = InlineKeyboardButton(text='Женский ♀', callback_data='female')
    markup = InlineKeyboardMarkup(inline_keyboard=[[male_button, female_button]])
    await message.answer(text='Укажите ваш пол:', reply_markup=markup)
    await state.set_state(FSMFitnessProfile.fill_gender)

# Предупреждение при неправильном вводе возраста
@router.message(StateFilter(FSMFitnessProfile.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть числом от 4 до 120. Попробуйте снова.\n\n'
             'Для отмены отправьте /cancel'
    )

# Обработка пола (через callback)
@router.callback_query(StateFilter(FSMFitnessProfile.fill_gender), F.data.in_(["male", "female"]))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками
    await callback.message.delete()
    await callback.message.answer(text='Введите ваш рост (в см):')
    await state.set_state(FSMFitnessProfile.fill_height)
    await callback.answer()

# Предупреждение при неправильном выборе пола
@router.message(StateFilter(FSMFitnessProfile.fill_gender))
async def warning_not_gender(message: Message):
    await message.answer(
        text='Пожалуйста, используйте кнопки для выбора пола.\n\nДля отмены отправьте /cancel'
    )

# Обработка роста
@router.message(StateFilter(FSMFitnessProfile.fill_height), F.text.isdigit(), lambda m: 100 <= int(m.text) <= 250)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer(text='Введите ваш вес (в кг):', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFitnessProfile.fill_weight)

@router.message(StateFilter(FSMFitnessProfile.fill_height))
async def warning_invalid_height(message: Message):
    await message.answer(text='Введите корректный рост (от 100 до 250 см).')

# Обработка веса
@router.message(StateFilter(FSMFitnessProfile.fill_weight), F.text.isdigit(), lambda m: 30 <= int(m.text) <= 300)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer(text='Выберите уровень активности:', reply_markup=activity_level_keyboard())
    await state.set_state(FSMFitnessProfile.fill_activity_level)

@router.message(StateFilter(FSMFitnessProfile.fill_weight))
async def warning_invalid_weight(message: Message):
    await message.answer(text='Введите корректный вес (от 30 до 300 кг).')

# Обработка уровня активности (через callback)
@router.callback_query(StateFilter(FSMFitnessProfile.fill_activity_level), F.data.in_(["beginner", "intermediate", "advanced"]))
async def process_activity_level(callback: CallbackQuery, state: FSMContext):
    activity_map = {
        'beginner': 'Начинающий',
        'intermediate': 'Средний',
        'advanced': 'Продвинутый'
    }
    await state.update_data(activity_level=activity_map.get(callback.data))
    await callback.message.edit_text(text='Выберите вашу цель:', reply_markup=goal_keyboard())
    await state.set_state(FSMFitnessProfile.fill_goal)
    await callback.answer()

# Обработка цели (через callback)
@router.callback_query(StateFilter(FSMFitnessProfile.fill_goal), F.data.in_(["weight_loss", "muscle_gain", "maintenance"]))
async def process_goal(callback: CallbackQuery, state: FSMContext):
    goal_map = {
        'weight_loss': 'Похудение',
        'muscle_gain': 'Набор массы',
        'maintenance': 'Поддержание формы'
    }
    await state.update_data(goal=goal_map.get(callback.data))
    await callback.message.edit_text(text='Есть ли у вас ограничения по здоровью?', reply_markup=health_restrictions_keyboard())
    await state.set_state(FSMFitnessProfile.fill_health_restrictions)
    await callback.answer()

# Обработка ограничений по здоровью (через callback)
@router.callback_query(StateFilter(FSMFitnessProfile.fill_health_restrictions), F.data.in_(["has_restrictions", "no_restrictions"]))
async def process_restrictions_choice(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'has_restrictions':
        await callback.message.edit_text(text='Опишите ваши ограничения:')
        await state.set_state(FSMFitnessProfile.fill_health_restrictions_text)
    else:
        await state.update_data(health_restrictions='Нет')
        await callback.message.edit_text(text='Выберите предпочитаемые активности:', reply_markup=activities_keyboard())
        await state.set_state(FSMFitnessProfile.select_activities)
    await callback.answer()

# Обработка текста ограничений
@router.message(StateFilter(FSMFitnessProfile.fill_health_restrictions_text), F.text)
async def process_restrictions_text(message: Message, state: FSMContext):
    await state.update_data(health_restrictions=message.text)
    await message.answer(text='Выберите предпочитаемые активности:', reply_markup=activities_keyboard())
    await state.set_state(FSMFitnessProfile.select_activities)

@router.message(StateFilter(FSMFitnessProfile.fill_health_restrictions_text))
async def warning_invalid_restrictions(message: Message):
    await message.answer(text='Пожалуйста, опишите ограничения текстом. Для отмены отправьте /cancel.')

# Обработка выбора активностей (через callback)
@router.callback_query(StateFilter(FSMFitnessProfile.select_activities))
async def process_activities(callback: CallbackQuery, state: FSMContext):
    # Здесь должна быть логика обработки выбранных активностей.
    # Например, можно собрать выбранные данные и сохранить их.
    await state.update_data(selected_activities=callback.data)
    await callback.message.edit_text(text='Профиль заполнен! Для просмотра отправьте /showdata')
    await state.clear()
    await callback.answer()

# Обработка команды /showdata
@router.message(Command("showdata"), StateFilter())
async def process_showdata_command(message: Message):
    user_id = message.from_user.id
    if user_id in user_dict:
        data = user_dict[user_id]
        profile_text = (
            f"Имя: {data.get('name', 'не указано')}\n"
            f"Возраст: {data.get('age', 'не указан')}\n"
            f"Пол: {data.get('gender', 'не указан')}\n"
            f"Рост: {data.get('height', 'не указан')}\n"
            f"Вес: {data.get('weight', 'не указан')}\n"
            f"Уровень активности: {data.get('activity_level', 'не указан')}\n"
            f"Цель: {data.get('goal', 'не указана')}\n"
            f"Ограничения: {data.get('health_restrictions', 'не указаны')}\n"
            f"Активности: {data.get('selected_activities', 'не указаны')}\n"
        )
        await message.answer(profile_text)
    else:
        await message.answer(text='Профиль не заполнен. Отправьте /profile для заполнения.')

# Эхо хэндлер, если команда не распознана
@router.message(StateFilter(), F.text)
async def send_echo(message: Message):
    await message.reply(text='Не понимаю. Используйте /profile для заполнения профиля.')
