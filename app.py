from aiogram import executor
from source import handlers
from source import middlewares
from source.handlers import dp
from aiogram import executor
from loguru import logger
import time

async def set_commands(dp):
    from aiogram import types

    await dp.bot.set_my_commands(
        commands=[
            types.BotCommand(command="/start", description="🏠 Главное меню"),
            #types.BotCommand(command="/send", description="📤 Отправить файл"),
        ]
    )


async def on_startup(dp):
    middlewares.setup(dp)
    await set_commands(dp)
    handlers.setup(dp)

    logger.add(
        f'logs/{time.strftime("%Y-%m-%d__%H-%M")}.log',
        level="DEBUG",
        rotation="500 MB",
        compression="zip",
    )

    logger.success("[+] Бот запущен!")

# Запуск бота
if __name__ == "__main__":
    # Launch
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)