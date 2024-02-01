from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

async def contact_kb():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.insert(KeyboardButton('📱 Отправить телефон', request_contact=True))
    return keyboard

async def list_orders_kb():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.insert(KeyboardButton('Мои заказ-наряды'))
    return keyboard

async def remove_kb():
    keyboard = ReplyKeyboardRemove()
    return keyboard

async def cancel_kb():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.insert(KeyboardButton('❌ Отменить ❌'))

