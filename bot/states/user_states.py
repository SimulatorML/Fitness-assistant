# bot/states/user_states.py
from aiogram.fsm.state import State, StatesGroup

class UserForm(StatesGroup):
    name = State()  # Ввод имени пользователя
    birth_date = State()  # Ввод даты рождения
    gender = State()  # Выбор пола
    height = State()  # Ввод роста
    weight = State()  # Ввод веса
    activity_level = State()  # Выбор уровня активности
    goal = State()  # Выбор цели
    health_restrictions = State()  # Ввод ограничений по здоровью
    preferred_activities = State()  # Ввод предпочтительных активностей
    confirm_profile = State()  # Подтверждение профиля
    select_activities = State() 