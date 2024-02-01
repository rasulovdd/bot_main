from loguru import logger
from aiogram import types
from source.middlewares import rate_limit
from source.api import onec
import source.database.db as db
from source.keyboard import reply, inline
import json
from time import sleep
import time
from source.utils import is_int
from loader import bot

@rate_limit(limit=1)
async def orders_list(message: types.Message):
    # обработка текста заказ-наряды
    user_id = message.from_user.id
    user_status = db.get_status(user_id)
    if user_status == 1 or user_status == 2:
        if message.text == "Мои заказ-наряды":
            # отправляем запрос 1С и получаем список заказ=нарядов
            status, result = onec.LastOrders(user_id)
            # устанавливаем статус 2 (работа с ЗН)  
            db.set_status(user_id, 2)
            await message.answer("Ваши заказ-наряды:", reply_markup=await reply.remove_kb())
            if status == 200:
                try:
                    data = json.loads(result)
                except ValueError as my_error:
                    logger.error(f"[-] Мои заказ-наряды. Ошибка: {my_error}")
                    await message.answer(
                        user_id, "Что-то пошло не так!\nНажмите /start и начните сначала")
                    return
                # вытаскиваем нужные данные из json
                for order in data["orders"]:
                    # выводим список заказ-нарядов
                    order_data = order['docdate']
                    order_data_text = order_data.split("T")
                    my_text = (
                        f"📑 Заказ №: {order['docnumber']}\n"
                        f"🗓 Дата: {order_data_text[0]} {order_data_text[1]}\n"
                        #f"🗓 Дата: {order['docdate']}\n"
                        f"🚘 VIN: <tg-spoiler>{order['vin']}</tg-spoiler>\n"
                        f"⚙️ Номер: {order['regn']}\n"
                        f"👤 Клиент: {order['name']}"
                    )
                    await message.answer(my_text, parse_mode="HTML", reply_markup=await inline.order_list(order['guid']))
                    # пауза после отправки сообщений чтобы не попасть в бан лист
                    sleep(0.05)
            else:
                await message.answer("Что-то пошло не так(")
        
        elif is_int(message.text):
            # отправляем запрос 1С и получаем заказ-наряд
            status, result = onec.Order(user_id, message.text)  
            # устанавливаем статус 2 (работа с ЗН) 
            db.set_status(user_id, 2)    
            if status == 200:
                try:
                    data = json.loads(result)
                except ValueError as my_error:
                    logger.error(f"[-] Заказ-наряд. Ошибка: {my_error}")
                    await message.answer(
                        user_id, "Что-то пошло не так!\nНажмите /start и начните сначала")
                    return
                # выводим заказ-наряд
                order_data = data['docdate']
                order_data_text = order_data.split("T")
                my_text = (
                    f"📑 Заказ №: {data['docnumber']}\n"
                    f"🗓 Дата: {order_data_text[0]} {order_data_text[1]}\n"
                    f"🚘 VIN: <tg-spoiler>{data['vin']}</tg-spoiler>\n"
                    f"⚙️ Номер: {data['regn']}\n"
                    f"👤 Клиент: {data['name']}"
                )
                await message.answer(my_text, parse_mode="HTML", reply_markup=await inline.order_list(data['guid']))
                
            else:
                await message.answer("Документ не обнаружен\nВведите номер заказ-наряда или начните все сначала нажав на кнопку /start")

        else:
            await message.answer(
                "Введите номер заказ-наряда или нажмите кнопку <b>Мои заказ-наряды</b>", 
                parse_mode="HTML", reply_markup=await reply.list_orders_kb())
    
    elif user_status == 0:
        await message.answer("Я Вас не понимаю(.\nНажмите кнопку 👇 или начните сначала нажав Меню->Start")

    # elif user_status == 2: # работа с заказ нарядом
    #     if is_int(message.text):
    #         # отправляем запрос 1С и получаем заказ-наряд
    #         status, result = onec.Order(user_id, message.text)      
    #         if status == 200:
    #             try:
    #                 data = json.loads(result)
    #             except ValueError as my_error:
    #                 logger.error(f"[-] Заказ-наряд. Ошибка: {my_error}")
    #                 await message.answer(
    #                     user_id, "Что-то пошло не так!\nНажмите /start и начните сначала")
    #                 return
    #             # выводим заказ-наряд
    #             order_data = data['docdate']
    #             order_data_text = order_data.split("T")
    #             my_text = (
    #                 f"📑 Заказ №: {data['docnumber']}\n"
    #                 f"🗓 Дата: {order_data_text[0]} {order_data_text[1]}\n"
    #                 f"🚘 VIN: <tg-spoiler>{data['vin']}</tg-spoiler>\n"
    #                 f"⚙️ Номер: {data['regn']}\n"
    #                 f"👤 Клиент: {data['name']}"
    #             )
    #             await message.answer(my_text, parse_mode="HTML", reply_markup=await inline.order_list(data['guid']))
                    
    #         else:
    #             await message.answer("Документ не обнаружен\nВведите номер заказ-наряда или начните все сначала нажав на кнопку /start")

    #     else:
    #         await message.answer(
    #             "Введите номер заказ-наряда или нажмите кнопку <b>Мои заказ-наряды</b>", 
    #             parse_mode="HTML", reply_markup=await reply.list_orders_kb())
    
    elif user_status == 3: #просим загрузить фото или видео  
        # удаление сообщения 
        # await message.delete()
        await message.answer("Загрузите пожалуйста фото или видео")

    elif user_status == 4: #ждем комментарий и загружаем контект в 1
        # получаем нужные данные из темп базы
        file_info = db.get_file_info(user_id)
        #устанавливаем статус 5
        db.set_status(user_id, 5)
        await bot.edit_message_text("Файл подготовлен к загрузке в 1С!\n"
                                "✅ Данные загружены успешно", user_id, file_info[4], reply_markup=None)
        # загружаем данные в 1С
        status, result, my_json = onec.Content(user_id, message.text, file_info)
        if status == 200:
            logger.success(f"[+] User ID: {user_id}. Отправил данные. {file_info}")
            await message.answer("✅ Успешно!\nХотите загрузить еще?", 
                                 reply_markup=await inline.yes_no(file_info[0],file_info[4]))
            # # убираем данные старого файла из базы
            # db.set_file_info(user_id,"","","")
            # удаляем старые данные 
            db.del_order_guid(user_id)
            #устанавливаем статус 3 
            db.set_status(user_id, 3)
        elif status == 404:
            await message.answer("❌ Документ не найден!")
            logger.error(f"[-] User ID: {user_id}. Не смог отправил данные. {file_info}")
        elif status == 500:
            await message.answer("❌ Что-то пошло не так!\nНажмите /start и начните сначала")
            logger.error(f"[-] User ID: {user_id}. Ошибка. [{result.reason}]. Данные [{my_json}]")

    elif user_status == 5: #просим завершить прежный статус
        # удаление сообщения 
        # await message.delete()
        await message.answer("Завершите пожалуйста предыдущую процедуру!")

@rate_limit(limit=1)
async def select_order(call: types.CallbackQuery):
    user_id = call.from_user.id
    order_guid = call.data.split('_')[1]
    # Бот Предлагает загрузить контент (фото или видео) или выбрать другой заказ-наряд
    db.set_status(user_id, 3) #устанавливаем статус 3
    # удаляем кнопку Выбрать
    await call.message.edit_reply_markup(reply_markup=await inline.selected_order())
    logger.info(f"[ ] Пользователь ID: {user_id} выбрал ЗН. guid: {order_guid}")
    # создаем кнопку Загрузить фото/видео
    await call.message.answer("Что Вы хотите сделать?", reply_markup=await inline.upload_content(order_guid, call.message.message_id))

@rate_limit(limit=1)
async def select_upload(call: types.CallbackQuery):
    user_id = call.from_user.id
    order_guid = call.data.split('_')[1]
    message_id = call.data.split('_')[2]
    #print (order_guid)
    # Записываем user_id и orders_guid в базу бота
    db.set_order_guid(user_id, order_guid, call.message.message_id)
    # меняем текст 
    await call.message.edit_text("Загрузите пожалуйста фото или видео", reply_markup=await inline.upload_cancel(message_id))

@rate_limit(limit=1)
async def selected_order(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, text='Заказ-наряд уже выбран')
    
@rate_limit(limit=1)
async def cancel_order(call: types.CallbackQuery):
    user_id = call.from_user.id
    logger.info(f"[ ] Выбор ЗН отменен.")
    message_id = call.data.split("_")[1]
    await call.message.edit_text("❌ Отменено",reply_markup=None)
    # устанавливаем статус 1
    db.set_status(user_id, 1) # режим выбора зн
    # удаляем tmp данные 
    db.del_order_guid(user_id)
    # удаляем сообщение 
    try:
        await bot.delete_message(user_id, message_id)
        logger.success(f"[ ] Сообщение id: {message_id} удалено.")
    except:
        logger.error(f"[-] Сообщение id. {message_id} не сущействует.")