from loader import db
from loguru import logger
from aiogram.types import Message
import sqlite3


async def add_user(message: Message) -> None:
    """
    Создает базу данных если её еще нет, таблицу с данными пользователей:
    id, username и, если есть, "имя фамилия" и добавляет туда данные, если
    бота запускает новый пользователь. Данная таблица не участвует в выдаче сохраненной
    информации. Она просто хранит данные пользователя.
    :param message:
    :return:
    """

    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        chat_id INTEGER UNIQUE,
        username STRING,
        fullname TEXT);   
    """)
    connection.commit()
    try:
        cursor.execute(
            "INSERT INTO user(chat_id, username, fullname) VALUES(?,?,?)",
            (message.chat.id, message.from_user.first_name, message.from_user.full_name)
        )
        connection.commit()
        logger.info(f'Пользователь с Username: {message.from_user.full_name} & User_id: {message.chat.id} создан.')
    except sqlite3.IntegrityError:
        logger.info(f'Данный пользователь уже существует. User_id: {message.chat.id}')
    connection.close()


async def add_query(query_data: dict) -> None:
    """
    Создаёт таблицу, если она ещё не создавалась и добавляет туда данные,
    которые ввел пользователь для поиска
    : param query_data : dict
    : return : None
    """
    user_id = query_data['chat_id']
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS query(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER,
        data_symbol STRING);    
    """)
    try:
        cursor.execute(
            "INSERT INTO query(user_id, data_symbol) VALUES (?, ?)",
            (
                user_id,
                query_data['data_symbol']
            )
        )
        logger.info(f'В БД добавлен новый запрос. User_id: {user_id}')

        # Нам не нужно очень много записей историй поиска, поэтому для каждого пользователя
        # будем хранить только 5 последних записей, лишние - удалим.
        cursor.execute(f"""
                DELETE FROM query WHERE `user_id` = '{user_id}'
                AND
                ((SELECT COUNT(*) FROM query WHERE `user_id` = '{user_id}' ) > 5 )
            """
                       )
        connection.commit()
    except sqlite3.IntegrityError:
        logger.info(f'Запрос с такой датой и временем уже существует. User_id: {user_id}')
    connection.close()


async def add_query_news(query_data: dict) -> None:
    """
    Создаёт таблицу, если она ещё не создавалась и добавляет туда данные,
    которые ввел пользователь для поиска новостей
    : param query_data : dict
    : return : None
    """
    user_id = query_data['user_id']
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS query_news(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTEGER,
        category_news STRING,
        quantity_news INTEGER,
        link_list STRING,
        date DATE
        );    
    """)
    try:
        cursor.execute(
            "INSERT INTO query_news(user_id, category_news, quantity_news, link_list, date) VALUES (?, ?, ?, ?, ?)",
            (
                user_id,
                query_data['category_news'],
                query_data['quantity_news'],
                query_data['link_list'],
                query_data['date'],
            )
        )
        logger.info(f'В БД добавлен новый запрос. User_id: {user_id}')
        connection.commit()
    except sqlite3.IntegrityError:
        logger.info(f'такой запрос уже существует от User_id: {user_id}')
    connection.close()
