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
