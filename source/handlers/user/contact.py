from loguru import logger
from aiogram import types
from loader import dp
from source.middlewares import rate_limit
from source.utils import mob_format
from source.api import onec
import source.database.db as db
from source.keyboard import reply

# Обработчик на прием файлов
@rate_limit(limit=1)
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def check_contact(message: types.Message):
    user_id = message.from_user.id
    user_status = db.get_status(user_id)
    if user_status == 0:
        phone_num = message.contact.phone_number
        my_number = mob_format(phone_num)
        contact_id = message.contact.user_id
        # проверяем id контакта
        if contact_id == user_id:
            # отправляем запрос 1С и определяем есть у пользователя доступ или нет
            result = onec.Login(my_number, user_id)
            if result == 200:
                await message.answer("Спасибо, Вы зарегистрированы!", reply_markup=await reply.list_orders_kb())
                db.set_status(user_id, 1)
                logger.success(f"[+] User ID: {user_id} зарегистрировался в 1С")

            elif result == 404 or result == 500:
                await message.answer("У Вас нет прав на регистрацию")
                logger.error(f"[+] User ID: {user_id} не смог зарегистрироваться в 1С, Ошибка [У Вас нет прав на регистрацию]")
        else:
            await message.answer("Это не ваш контакт!\nОтправьте свой контакт пожалуйста")
            logger.error(f"[-] User ID: {user_id} пытался отправить не свой контакт")
    else:
        await message.answer("Вы уже зарегистрированы!")
        logger.info(f"[ ] User ID: {user_id} уже зарегистрирован")
