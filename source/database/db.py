""" Модуль для работы с db """
from loguru import logger
from source.data import config
from mysql.connector import MySQLConnection, Error  # Добавляем функцию MySQLConnection


db_config = config.database_connection_parameters  # получаем настройки для подключения к БД
#print (db_config)

def is_user_exists(user_id):
    """ сушествует ли пользователь """
    status=''
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = (f"SELECT 1 FROM users WHERE user_id='{user_id}'")
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            status = row[0]
        else:
            status = 0
        cursor.close()
    except Error as error:
        logger.error(f"[-] Ошибка. {error}")
    conn.close()  # Закрываем соединение
    return status

def set_user_id(user_id):
    """ Записываем UserID при старте """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # открывем соединение
        # отправляем запрос
        cursor.execute("INSERT INTO users (user_id) VALUES (%s)",(user_id,))
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] Пользователь с ID {user_id} добавлен!")
    except Error as error:
        logger.error(f"[-] Ошибка при добавление пользователя с ID {user_id}. {error}")

    conn.close()  # Закрываем соединение

def set_status(user_id, status):
    """ устанавливаем статус """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(f"UPDATE users SET status='{status}' WHERE user_id='{user_id}'")
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] Статус пользователя с ID {user_id} изменен на {status}.")
    except Error as error:
        logger.error(f"[-] Ошибка при обновление статус пользователя с ID {user_id}. {error}")
    conn.close()  # Закрываем соединение

def get_status(user_id):
    """ Получить статус по user_id """
    status=''
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = (f"SELECT status FROM users WHERE user_id='{user_id}'")
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            status = row[0]
        else:
            status = 0
        cursor.close()
        logger.info(f"[ ] Статус пользователя с ID {user_id} = {status}.")
    except Error as error:
        logger.error(f"[-] Ошибка при получение статуса пользователя с ID {user_id}. {error}")
    conn.close()  # Закрываем соединение
    return status

def set_order_guid(user_id, orders_guid, message_id):
    """ Записываем user_id, orders_guid, message_id в базу бота """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # открывем соединение
        # отправляем запрос
        cursor.execute("INSERT INTO tmp (user_id, orders_guid, message_id) VALUES (%s,%s,%s)",
                       (user_id, orders_guid, message_id))
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] Данные записаны. ID: {user_id}. [{orders_guid},{message_id}]")
    except Error as error:
        logger.error(f"[-] Ошибка при добавление данных. ID:{user_id}. [{orders_guid},{message_id}]. {error}")
    conn.close()  # Закрываем соединение

def del_order_guid(user_id):
    """ удаляем user_id и orders_guid из базу бота """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(f"DELETE FROM tmp WHERE user_id='{user_id}'")  # Выполняем запрос
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] Данные из tmp удалены. ID: {user_id}")
    except Error as error:
        logger.error(f"[-] Ошибка при удаление данных. ID: {user_id} | {error}")
    conn.close()  # Закрываем соединение

def set_file_info(user_id, file_ext, file_type, file_path):
    """ записываем file_ext, file_type, file_path """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(
            f"UPDATE tmp SET file_ext='{file_ext}', file_type='{file_type}', file_path='{file_path}' "
            f"WHERE user_id='{user_id}'")
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] User id: {user_id}. Данные добавлены. [{file_ext}, {file_type}, {file_path}]")
    except Error as error:
        logger.error(f"[-] Ошибка при добавление данных. [{file_ext}, {file_type}, {file_path}]. {error}")
    conn.close()  # Закрываем соединение

def set_message_id(user_id, message_id):
    """ записываем message_id """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(
            f"UPDATE tmp SET message_id='{message_id}' WHERE user_id='{user_id}'")
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] User id: {user_id}. Данные добавлены. [{message_id}]")
    except Error as error:
        logger.error(f"[-] Ошибка при добавление данных. [{message_id}]. {error}")
    conn.close()  # Закрываем соединение

def get_message_id(user_id):
    """ получаем message_id """
    message_id=''
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = (
            f"SELECT message_id FROM tmp WHERE user_id='{user_id}'")
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            message_id = row[0]
        else:
            message_id = 0
        cursor.close()
        logger.success(f"[+] User ID:{user_id}. Получил данные: [{message_id}]")
    except Error as error:
        logger.error(f"[-] User ID:{user_id} не смог получить данные. {error}")
    conn.close()  # Закрываем соединение
    return message_id

def get_file_info(user_id):
    """ получаем orders_guid, file_ext, file_type, file_path, message_id """
    file_info=''
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = (
            f"SELECT orders_guid, file_ext, file_type, file_path, message_id "
            f"FROM tmp WHERE user_id='{user_id}'")
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            file_info = row
        else:
            file_info = 0
        cursor.close()
        logger.success(f"[+] User ID:{user_id}. Получил данные: [{file_info}]")
    except Error as error:
        logger.error(f"[-] User ID:{user_id} не смог получить данные. {error}")
    conn.close()  # Закрываем соединение
    return file_info