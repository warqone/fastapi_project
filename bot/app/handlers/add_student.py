import logging

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards import builders
from app.services import api
from app.texts import texts

logger = logging.getLogger(__name__)
add_student_router = Router()


class AddStudent(StatesGroup):
    """Состояния для добавления студента."""
    first_name = State()
    last_name = State()
    status = State()
    email = State()
    gpa = State()
    birth_date = State()


@add_student_router.callback_query(F.data == 'add_student')
async def add_student(call: types.CallbackQuery, state: FSMContext):
    """Начало добавления студента. Предложение ввести имя студента."""
    await call.message.edit_text('Введите имя студента')
    await state.set_state(AddStudent.first_name)


@add_student_router.message(StateFilter(AddStudent.first_name))
async def add_student_first_name(message: types.Message, state: FSMContext):
    """Ввод имени студента."""
    await state.update_data(first_name=message.text)
    await message.answer('Введите фамилию студента')
    await state.set_state(AddStudent.last_name)


@add_student_router.message(StateFilter(AddStudent.last_name))
async def add_student_last_name(message: types.Message, state: FSMContext):
    """Ввод фамилии студента."""
    await state.update_data(last_name=message.text)
    await message.answer(
        'Выберите статус студента',
        reply_markup=builders.select_student_status_kb())
    await state.set_state(AddStudent.status)


@add_student_router.callback_query(StateFilter(AddStudent.status))
async def add_student_status(call: types.CallbackQuery, state: FSMContext):
    """Выбор статуса студента."""
    status = call.data.split('-')[1]
    await state.update_data(status=status)
    await call.message.edit_text(
        'Введите email студента (user@example.com)')
    await state.set_state(AddStudent.email)


@add_student_router.message(StateFilter(AddStudent.email))
async def add_student_email(message: types.Message, state: FSMContext):
    """Ввод email студента."""
    await state.update_data(email=message.text)
    await message.answer('Введите средний балл студента')
    await state.set_state(AddStudent.gpa)


@add_student_router.message(StateFilter(AddStudent.gpa))
async def add_student_gpa(message: types.Message, state: FSMContext):
    """Ввод среднего балла студента."""
    await state.update_data(gpa=int(message.text))
    await message.answer(
        'Выберите дату рождения студента (YYYY-MM-DD)')
    await state.set_state(AddStudent.birth_date)


@add_student_router.message(StateFilter(AddStudent.birth_date))
async def add_student_birth_date(message: types.Message, state: FSMContext):
    """Ввод даты рождения студента.
    Сохранение данных в базу данных и вывод сообщения об успехе."""

    birth_date = message.text
    await state.update_data(birth_date=birth_date)
    data = await state.get_data()

    try:
        response = await api.create_student(data)
        logger.info(f'Студент {data} добавлен в базу данных.')
        student_id = response['id']
        await message.answer(
            texts.succesfull_add_msg.format(id=student_id),
            reply_markup=builders.main_menu_kb())

    except Exception as e:
        logger.error(f'Ошибка при добавлении студента: {e}')
        await message.answer(
            texts.error_msg,
            reply_markup=builders.main_menu_kb())

    await state.clear()
