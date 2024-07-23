from loader import db
from loguru import logger
import sqlite3


async def read_query(user: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    logger.info(f'Читаем таблицу query. User_id: {user}')
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT `data_symbol` FROM query WHERE `user_id` = ? ORDER BY id DESC LIMIT 1", (user,))
        records = cursor.fetchall()
        connect.close()
        return records
    except sqlite3.OperationalError:
        logger.info(f"В базе данных пока нет таблицы с запросами. User_id: {user}")
        return []



async def read_query_news(user: int) -> list:
    """
        Принимает id пользователя, делает запрос к базе данных, получает в ответ
        результаты запросов данного пользователя.
        : param user : int
        : return : list
    """
    logger.info(f'Читаем таблицу query_news. User_id: {user}')
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT * FROM query_news WHERE `user_id` = ?", (user,))
        records = cursor.fetchall()
        connect.close()
        return records
    except sqlite3.OperationalError:
        logger.info(f"В базе данных пока нет таблицы с запросами. User_id: {user}")
        return []