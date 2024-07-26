from aiogram.filters.state import State, StatesGroup


class UserState(StatesGroup):
    analysis_state_callback = State()
    news_state_callback = State()
    symbol_for_analysis_state = State()  # Состояния для поиска тикера
    analysis_state = State()  # Состояние выдачи аналитики
    symbol_for_news_state = State()  # Состояния для поиска тикера
    var_news_state = State()  # Состояние вылова колбека не по тикеру, и запрос новости
    ticker_news_state = State()  # Состояние вылова новостей по тикеру
    number_for_ticker_news = State()  # Запрос кол-ва новостей и их вывод
