from aiogram import Dispatcher
from loguru import logger
from aiogram import types

from .start import *
from .contact import *
from .orders import *
from .upload_s3 import *

def register_user_handlers(dp: Dispatcher):
    try:
        dp.register_message_handler(start, commands=["start", "menu"], state="*")

        #dp.message_handler(check_contact, content_types=types.ContentType.CONTACT, state="*")

        dp.register_message_handler(orders_list, state="*")

        dp.register_callback_query_handler(
            select_order,
            lambda call: call.data.startswith("order_"),
            state="*",
        )
        dp.register_callback_query_handler(
            select_upload,
            lambda call: call.data.startswith("upload_"),
            state="*",
        )
        dp.register_callback_query_handler(
            selected_order,
            lambda call: call.data.startswith("selected_order_"),
            state="*",
        )
        dp.register_callback_query_handler(
            cancel_order,
            lambda call: call.data.startswith("cancel_"),
            state="*",
        )
        dp.register_callback_query_handler(
            cansel_upload,
            lambda call: call.data.startswith("cancel1c_"),
            state="*",
        ) 
        dp.register_callback_query_handler(
            upload_to_1c,
            lambda call: call.data.startswith("upload1c_"),
            state="*",
        )
        dp.register_callback_query_handler(
            button_yes,
            lambda call: call.data.startswith("yes_"),
            state="*",
        )
        dp.register_callback_query_handler(
            button_no,
            lambda call: call.data.startswith("no_"),
            state="*",
        )


    except Exception as e:
        logger.error(f"[-] Ошибка при регистрации user handlers: {e}")
    else:
        logger.info("[ ] User handlers зарегистрированы")