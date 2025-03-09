from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional

def gender_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора пола."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='♂ Мужской', callback_data='male'),
         InlineKeyboardButton(text='♀ Женский', callback_data='female')]
    ])
    return keyboard

def activity_level_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора уровня активности."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Начинающий', callback_data='beginner')],
        [InlineKeyboardButton(text='Средний', callback_data='intermediate')],
        [InlineKeyboardButton(text='Продвинутый', callback_data='advanced')]
    ])
    return keyboard

def goal_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора цели."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Похудение', callback_data='weight_loss')],
        [InlineKeyboardButton(text='Набор массы', callback_data='muscle_gain')],
        [InlineKeyboardButton(text='Поддержание формы', callback_data='maintenance')]
    ])
    return keyboard

def health_restrictions_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса о наличии ограничений по здоровью."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='has_restrictions')],
        [InlineKeyboardButton(text='Нет', callback_data='no_restrictions')]
    ])
    return keyboard

def activities_keyboard(selected_activities: Optional[List[str]] = None) -> InlineKeyboardMarkup:
    """Клавиатура для выбора предпочитаемых активностей."""
    if selected_activities is None:
        selected_activities = []

    all_activities = {
        'running': '🏃 Бег',
        'swimming': '🏊 Плавание',
        'gym': '🏋️ Тренажерный зал',
        'yoga': '🧘 Йога',
        'cycling': '🚴 Велоспорт',
        'football': '⚽️ Футбол',
        'basketball': '🏀 Баскетбол',
        'volleyball': '🏐 Волейбол',
        'tennis': '🎾 Теннис'
    }
    keyboard_rows = []

    # Формируем ряды по 2 кнопки
    activity_ids = list(all_activities.keys())
    for i in range(0, len(activity_ids), 2):
        row = []
        for activity_id in activity_ids[i:i + 2]:
            prefix = "✅ " if activity_id in selected_activities else ""
            row.append(InlineKeyboardButton(
                text=f"{prefix}{all_activities[activity_id]}",
                callback_data=activity_id  # Без префикса
            ))
        keyboard_rows.append(row)

    keyboard_rows.append([
        InlineKeyboardButton(text="➡️ Продолжить", callback_data="activities_done")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

def confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения профиля."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm')],
        [InlineKeyboardButton(text='🔄 Редактировать', callback_data='edit')]
    ])
    return keyboard