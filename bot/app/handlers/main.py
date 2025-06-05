from aiogram import Router, F, types
from aiogram.filters import Command

from app.keyboards.builders import main_menu_kb
from app.texts.texts import main_menu_msg, hello_msg

main_router = Router()


@main_router.message(Command(commands=['start']))
async def start(message: types.Message):
    """Обрабатывает ввод команды /start."""
    await message.answer(
        hello_msg.format(name=message.from_user.first_name),
        reply_markup=main_menu_kb()
    )


@main_router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback: types.CallbackQuery):
    """Обрабатывает выбор пункта меню "Назад в главное меню"."""
    await callback.message.edit_text(
        main_menu_msg,
        reply_markup=main_menu_kb()
    )
