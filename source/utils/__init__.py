
from loguru import logger
import os

def is_int(text):
    return text.isdigit()

def mob_format(s):
    """ получение номера телефона в нужном формате"""
    number = s
    my_number = 0
    if len(number) > 11:
        my_number = number[:0] + "" + number[1:]
        my_number = my_number[:0] + "7" + my_number[1:]
    else:
        my_number = number[:0] + "7" + number[1:]
    return my_number

async def delete_files(file_path):
    """ Удаление файлов. 
        Проверяем, существует ли файл, прежде чем удалить его """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.success(f'[+] Файл {file_path} успешно удален')
        else:
            logger.error(f'[-] Файл {file_path} не существует')
    except Exception as e:
        logger.error(f'[-] Произошла ошибка при удаление файла: {str(e)}')