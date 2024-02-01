from loguru import logger
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
import source.database.db as db

from source.handlers.user.check_is_user_admin import is_admin
from source.keyboard import reply
#from loader import db_manager

from source.middlewares import rate_limit

@rate_limit(limit=1)
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"[ ] User ID: {user_id} запустил бота")

    if not db.is_user_exists(user_id):
        new_user = True
    else:
        new_user = False

    if new_user:    
        await message.answer(
            'Привет! Поделитесь с контактом и я проверю Ваш доступ.\nНажмите кнопку <b>Отправить телефон 👇</b>', 
            parse_mode="HTML",reply_markup=await reply.contact_kb()
        )
        # если пользователь новый добавляем данные в таблицу и устанавливаем статус 0
        db.set_user_id(user_id)
        db.set_status(user_id, 0)
    else:
        # проверяем статус для определение какую клавиатуру показывать. 
        status = db.get_status(user_id)
        if status == 0:
            await message.answer('Привет! Рад видеть Вас снова.')
            await message.answer(
                'Поделитесь с контактом и я проверю Ваш доступ.\nНажмите кнопку <b>Отправить телефон 👇</b>', 
                parse_mode="HTML",reply_markup=await reply.contact_kb())
        elif status == 1:
            await message.answer('Привет! Рад видеть Вас снова.', reply_markup=await reply.list_orders_kb())
            # удаляем tmp данные 
            db.del_order_guid(user_id)
        else:
            # cбрасываем статус пользователя
            db.set_status(user_id, 1)
            # удаляем tmp данные 
            db.del_order_guid(user_id)
            await message.answer('Привет! Рад видеть Вас снова.', reply_markup=await reply.list_orders_kb())
            
    await state.finish()

        
