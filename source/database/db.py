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
        conn.close()  # Закрываем соединение
    except Error as error:
        logger.error(f"[-] Ошибка. {error}")
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
        conn.close()  # Закрываем соединение
        logger.success(f"[+] Пользователь с ID {user_id} добавлен!")
    except Error as error:
        logger.error(f"[-] Ошибка при добавление пользователя с ID {user_id}. {error}")
    
def set_status(user_id, status):
    """ устанавливаем статус """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(f"UPDATE users SET status='{status}' WHERE user_id='{user_id}'")
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Статус пользователя изменен на {status}.")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при обновление статус пользователя. {error}")

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
        conn.close()  # Закрываем соединение
        logger.info(f"[ ] UserID: {user_id}. Статус пользователя = {status}.")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при получение статуса пользователя. {error}")
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
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Данные записаны [set_order_guid]")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при добавление данных. [set_order_guid]. {error}")
    
def del_order_guid(user_id):
    """ удаляем user_id и orders_guid из базу бота """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(f"DELETE FROM tmp WHERE user_id='{user_id}'")  # Выполняем запрос
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Данные из tmp удалены.")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при удаление данных | {error}")

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
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Данные добавлены. [set_file_info]")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при добавление данных. [set_file_info]. {error}")

def set_message_id(user_id, message_id):
    """ записываем message_id """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(
            f"UPDATE tmp SET message_id='{message_id}' WHERE user_id='{user_id}'")
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Данные добавлены. [{message_id}]")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при добавление данных. [{message_id}]. {error}")

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
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID:{user_id}. Получил данные: [{message_id}]")
    except Error as error:
        logger.error(f"[-] UserID:{user_id} не смог получить данные. {error}")
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
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID:{user_id}. Получил данные: [{file_info}]")
    except Error as error:
        logger.error(f"[-] UserID:{user_id} не смог получить данные. {error}")
    return file_info

def set_order_db(user_id, data, tmp):
    """ Записываем ЗН в таблицу orders """
    orders = []
    conn = MySQLConnection(**db_config)  # открывем соединение
    try:
        for order in data["orders"]:
            orders.append((
                user_id,
                order['docnumber'], 
                order['docdate'], 
                order['guid'], 
                order['model'],
                order['regn'],
                order['vin'],
                tmp,
            ))
        cursor = conn.cursor()  # открывем курсор
        cursor.executemany("INSERT INTO orders "
                           "(user_id, docnumber, docdate, guid, model, regn, vin, tmp) VALUES "
                           "(%s,%s,%s,%s,%s,%s,%s,%s)", orders)
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        logger.success(f"[+] UserID:{user_id}. Добавил ЗН в базу.")
    except Error as error:
        conn.rollback()
        logger.error(f"[-] UserID:{user_id}. Не смог добавить ЗН. Ошибка [{error}]") 
    conn.close()  # Закрываем соединение

def del_order_db(user_id, tmp):
    """ удаляем user_id и orders_guid из базу бота """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # Открываем курсор
        cursor.execute(f"DELETE FROM orders WHERE user_id='{user_id}' and tmp='{tmp}'")  # Выполняем запрос
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Данные из orders удалены. [tmp={tmp}]")
    except Error as error:
        logger.error(f"[-] UserID: {user_id}. Ошибка при удаление данных. | {error}")

def set_order_message_id(user_id, message_id, tmp):
    """ записываем message_id для удаления """
    try:
        conn = MySQLConnection(**db_config)  # открывем соединение
        cursor = conn.cursor()  # открывем соединение
        # отправляем запрос
        cursor.execute("INSERT INTO orders (user_id, message_id, tmp) VALUES (%s,%s,%s)",
                       (user_id, message_id, tmp))
        conn.commit()  # Подтверждаем изменения
        cursor.close()  # Закрываем курсор
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID: {user_id}. Данные записаны. [{user_id, message_id, tmp}]")
    except Error as error:
        logger.error(f"[-] UserID:{user_id}. Ошибка при добавление данных. [{user_id, message_id, tmp}]. {error}")   

def get_message_id_temp(user_id, tmp):
    """ получаем message_id для удаления"""
    message_id=[]
    try:
        #dbconfig = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT message_id FROM orders WHERE user_id='{user_id}' AND tmp={tmp}")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                message_id.append(row[0])
        else:
            message_id = []
        cursor.close()
        conn.close()  # Закрываем соединение
        logger.info(f"[ ] UserID: {user_id}. [message_id получен]")
    except Error as error:
        logger.error(f"[-] UserID:{user_id}. [Ошибка при получение message_id]. {error}") 
    
    return message_id

def get_orders_info(user_id, tmp, limit_from, limit_to):
    """ получаем docnumber, docdate, guid """
    my_orders = []
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT docnumber, docdate, guid "
            "FROM orders "
            f"WHERE user_id='{user_id}' AND tmp='{tmp}' "
            f"LIMIT {limit_from},{limit_to}"
            #f"Order BY STR_TO_DATE(date, '%d.%m.%Y') {sort} LIMIT {limit_from},{limit_to}"
        )
        rows = cursor.fetchall()
        if rows:
            my_orders = rows
        else:
            my_orders = []
        cursor.close()
        conn.close()  # Закрываем соединение
        logger.info(f"[ ] UserID: {user_id}. [get_orders_info получен]")
    except Error as error:
        logger.error(f"[-] UserID:{user_id}. [Ошибка при получение get_orders_info]. {error}") 
    
    return my_orders

def get_ordermini_info(user_id, guid):
    """ получаем docnumber, docdate, guid, model, regn, vin """
    ordermini_info=''
    try:
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        query = (
            f"SELECT docnumber, docdate, guid, model, regn, vin "
            f"FROM orders WHERE guid='{guid}' and tmp='0'")
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            ordermini_info = row
        else:
            ordermini_info = 0
        cursor.close()
        conn.close()  # Закрываем соединение
        logger.success(f"[+] UserID:{user_id}. Получил данные: [{ordermini_info}]")
    except Error as error:
        logger.error(f"[-] UserID:{user_id} не смог получить данные. {error}")
    return ordermini_info

    #test