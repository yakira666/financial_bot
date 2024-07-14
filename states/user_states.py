from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    symbol_for_news = State()
    symbol_for_analysis = State()
    news = State()
    analysis = State()
