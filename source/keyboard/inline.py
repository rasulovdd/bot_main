from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def order_list(guid):
    """ выбрать заказ-наряд """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="Выбрать",
            callback_data=f'order_{guid}'
        ),
    ]

    for button in buttons:
        keyboard.insert(button)
    return keyboard

async def selected_order():
    """ выбранный заказ-наряд """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="✅ Выбранный заказ-наряд",
            callback_data=f'selected_order_ok'
        ),
    ]

    for button in buttons:
        keyboard.insert(button)
    return keyboard

async def upload_content(guid, message_id):
    """ начать режим загрузки в S3 """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="📤 Загрузить фото/видео",
            callback_data=f'upload_{guid}_{message_id}'
        ),
        InlineKeyboardButton(
            text="❌ Отменить",
            callback_data=f'cancel_{message_id}'
        ),
    ]

    for button in buttons:
        keyboard.insert(button)
    return keyboard

async def upload_cancel(message_id):
    """ отменить режим загрузки """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="❌ Отменить",
            callback_data=f'cancel_{message_id}'
        ),
    ]
    for button in buttons:
        keyboard.insert(button)
    return keyboard

async def upload_1c():
    """ записать данные в 1С """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="💬 Оставить коммент и Загрузить",
            callback_data=f'upload1c_ok'
        ),
        InlineKeyboardButton(
            text="❌ Отменить",
            callback_data=f'cancel1c_ok'
        ),
    ]

    for button in buttons:
        keyboard.insert(button)
    return keyboard

async def upload_1c_cancel():
    """ отменить """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="❌ Отменить",
            callback_data=f'cancel1c_ok'
        ),
    ]

    for button in buttons:
        keyboard.insert(button)
    return keyboard

async def yes_no(guid, message_id):
    """ записать данные в 1С """
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text="📤 Загрузить фото/видео",
            callback_data=f'upload_{guid}_{message_id}'
        ),
        InlineKeyboardButton(
            text="❌ Нет",
            callback_data=f'no_ok'
        ),
    ]

    for button in buttons:
        keyboard.insert(button)
    return keyboard