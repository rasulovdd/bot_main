from loguru import logger
from aiogram import types
from loader import dp
from source.middlewares import rate_limit
from source.api import onec
import source.database.db as db
from loader import bot
from source.utils import delete_files
import time
from source.data import config, s3
from source.keyboard import inline, reply

# Обработчик на прием видео и фото
@rate_limit(limit=1)
@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def upload_s3_file(message: types.Message):
    user_id = message.from_user.id
    status = db.get_status(user_id)
    # определяем тип файла
    file = message.document or message.video or message.photo[-1]
    file_id = file.file_id
    file_info = await bot.get_file(file_id)
    file_name = file_info.file_path.split('/')[-1]
    #проверяем есть ли у пользователя уже загруженный файл
    file_info_db=db.get_file_info(user_id)
    if file_info_db[1]:
        # у пользователя уже есть подготовленный файл надо завершить работу с ней 
        await message.answer("Ошибка: У Вас уже есть открытый процесс загрузки, "
                             "Завершите её или отмените. Если ничего не видите нажмите "
                             "/start и начните все сначала.")
    else:
        if status == 3:
            logger.info(f"[ ] Пользователь с ID: {user_id}, отправил файл. {file_name}")
            message_id = db.get_message_id(user_id)
            # удаляем сообщение (загрузите фото или видео)
            try:
                await bot.delete_message(user_id, message_id)
                logger.success(f"[ ] Сообщение id: {message_id} удалено.")
            except:
                logger.error(f"[-] Сообщение id. {message_id} не сущействует.")
            #выполняем определенную команду в зависимости от типа файла
            if message.video:
                # код, который будет выполняться для видео
                file_type = "video"
            elif message.photo:
                # код, который будет выполняться для фото
                file_type = "photo"
            
            await message.reply(f"Тип файла: {file_type}\nГотовлю файл к загрузки на сервер ...")
            logger.info(f"[ ] Начинаю загрузку файла {file_name} на S3 ...")
            
            # уже не ныжный блок, так как локальный бот апи уже загрузил файл в папку
            # # загружаем файл в папку uploads
            # try:
            #     await bot.download_file_by_id(file_id, destination=f"{UPLOADS_FOLDER}/{file_name}")
            #     logger.success(f"[+] Файл {file_name} загружен в папку: {UPLOADS_FOLDER}")
            # except Exception as e:
            #     await message.reply(f'Произошла ошибка при загрузке файла: {str(e)}')
            #     logger.error(f'[-] Произошла ошибка при загрузке файла: {str(e)}')
            # -------------------------------------------------------------------------

            # Загрузите файл на S3
            try:
                # если надо создать папку и на S3 то вместо file_name вводим file_path
                #s3_key = f"{datetime.datetime.now().strftime('%d%m%y_%H%M%S')}_{file_name}"
                s3_key = f"{time.strftime('%d%m%y_%H%M%S')}_{file_name}"
                s3.upload_file(Filename=file_info.file_path, Bucket=config.s3_params['S3_BUCKET'], Key=s3_key, ExtraArgs={'ACL': 'public-read'})
                # await message.reply(f"Файл успешно загружен!\n{config.s3_params['S3_WEB']}/{s3_key}")
                await message.reply(
                    f"Файл подготовлен к загрузке в 1С!\nЖелаете оставить комментарий?",
                    reply_markup=await inline.upload_1c())
                logger.success(f'[+] Файл успешно загружен на S3, путь к файлу: {file_info.file_path}') 
                # записываем данные в темп базу
                file_path = f"https://{config.s3_params['S3_WEB']}/{s3_key}"
                db.set_file_info(user_id, f".{file_name.split('.')[1]}", file_type, file_path)
            except Exception as e:
                await message.reply(f'Произошла ошибка при загрузке файла на S3')
                logger.error(f'[-] Произошла ошибка при загрузке файла: {str(e)}')
            # удаляем файл
            await delete_files(file_info.file_path)
        
        elif status == 0:
            await message.answer("Вы не зарегистрированы. Прошу сперва зарегистрируйтесь!")
            logger.info(f"[ ] Не зарегистрированный пользователь с ID: {user_id}, отправил файл. {file_name}")
            #удаляем файл 
            await delete_files(file_info.file_path)
        else:
            await message.answer("Заказ-наряд не выбран. Прошу сперва выберите заказ наряд")
            logger.info(f"[ ] Пользователь с ID: {user_id}, отправил файл. {file_name}. Заказ-наряд не выбран")
            #удаляем файл 
            await delete_files(file_info.file_path)

@rate_limit(limit=1)
# Обработчик на прием файлов
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def process_file_doc(message: types.Message):
    user_id = message.from_user.id
    status = db.get_status(user_id)
    # определяем тип файла
    file = message.document
    file_id = file.file_id
    file_info = await bot.get_file(file_id)
    if status == 3:
        file_type = "Документ"
        await message.reply(f"Тип файла: {file_type}\nНе поддерживается")
        await message.answer('Отправьте пожалуйста фото или видео')
        logger.info(f"[-] Отправлен не поддерживаемый формат файла [{file_type}]")
        # удаляем файл
        await delete_files(file_info.file_path)
    else:
        # удаляем файл
        await delete_files(file_info.file_path)
       
@rate_limit(limit=1)
async def upload_to_1c(call: types.CallbackQuery):
    """ Загрузка инфы в 1С """
    user_id = call.from_user.id
    # устанавливаем статус 4 (ждем коммент)
    db.set_status(user_id, 4)
    # #меняем клавиатуру
    # await call.message.edit_reply_markup(reply_markup=await inline.upload_1c_cancel())
    await call.message.edit_text("Файл подготовлен к загрузке в 1С!\n"
                                 "Жду комментарий ...", reply_markup=await inline.upload_1c_cancel())
    #просим написать комментарий
    await call.message.answer('Напишите пожалуйста комментарий:')
    # обновляем message_id
    db.set_message_id(user_id, call.message.message_id)

@rate_limit(limit=1)
async def cansel_upload(call: types.CallbackQuery):
    """ Отмена загрузки данных в 1С """
    user_id = call.from_user.id
    logger.info(f"[ ] Загрузка инфо в 1С отменена.")
    #message_id = db.get_message_id(user_id)
    await call.message.edit_text("❌ Загрузка отменена",reply_markup=None)
    # устанавливаем статус 1
    db.set_status(user_id, 1) # режим выбора зн
    # удаляем tmp данные 
    db.del_order_guid(user_id)
    await call.message.answer("Вы вернулись в главное меню", reply_markup=await reply.list_orders_kb())

@rate_limit(limit=1)
async def button_yes(call: types.CallbackQuery):
    """ Отправить еще фото или видео """
    print ("yes")

@rate_limit(limit=1)
async def button_no(call: types.CallbackQuery):
    """ Отправить еще фото или видео """
    user_id = call.from_user.id
    logger.info(f"[ ] Загрузка доп файла в 1С отменена.")
    #message_id = db.get_message_id(user_id)
    await call.message.edit_text("✅ Успешно!\n❌ Загрузка доп файла отменена",reply_markup=None)
    # устанавливаем статус 1
    db.set_status(user_id, 1) # режим выбора зн
    # удаляем tmp данные 
    db.del_order_guid(user_id)
    await call.message.answer("Вы вернулись в главное меню", reply_markup=await reply.list_orders_kb())
