from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    start = State()  # Первоначальное состояние
    symbol_for_analysis = State()  # Состояния для поиска тикера
    analysis = State()  # Состояние выдачи аналитики
    symbol_for_news = State()  # Состояния для поиска тикера
    news = State()  # Состояние выдачи новостей

