from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    start_state = State()  # Первоначальное состояние
    symbol_for_analysis_state = State()  # Состояния для поиска тикера
    analysis_state = State()  # Состояние выдачи аналитики
    symbol_for_news_state = State()  # Состояния для поиска тикера
    var_news_state = State()  #
    news_state = State()  # Состояние выдачи новостей
    number_of_news = State ()  # Запрос кол-ва новостей
