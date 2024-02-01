from loguru import logger
from aiogram import types
from aiogram.dispatcher import FSMContext

from source.data import config
from source.keyboard import reply

def is_admin(func):
    async def wrapped(message: types.Message, state: FSMContext):
        if message.from_user.id in config.admins_ids:
            await func(message, state)
        else:
            await message.answer("У вас нет разрешения на использование этой команды.\n\n"
                                 "Обратись к @RasulovDD для получения дополнительной информации.",
                                 reply_markup=await reply.remove_kb())
    return wrapped