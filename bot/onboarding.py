from aiogram.fsm.state import State, StatesGroup


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
