import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import config
from app.handlers.add_student import add_student_router
from app.handlers.edit_student import edit_student_router
from app.handlers.main import main_router
from app.handlers.students import students_router


async def on_startup(bot: Bot):
    await bot.send_message(config.ADMIN_ID, text='Бот запущен.')


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    await bot.send_message(config.ADMIN_ID, text='Бот остановлен.')
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()


async def start():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode='HTML')
    )
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(add_student_router)
    dp.include_router(edit_student_router)
    dp.include_router(main_router)
    dp.include_router(students_router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    logger = logging.getLogger(__name__)
    asyncio.run(start())
