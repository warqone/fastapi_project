import logging

from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keyboards import builders
from app.services import api
from app.texts import texts


logger = logging.getLogger(__name__)
edit_student_router = Router()


@edit_student_router.callback_query(F.data.startswith('edit_student_'))
async def edit_student(call: types.CallbackQuery, state: FSMContext):
    """Редактирование студента.
    Выводит информацию о студенте и кнопки для редактирования."""

    student_id = int(call.data.split('_')[-1])

    data = await state.get_data()
    students: list[dict] = data.get('students', [])

    student = next((s for s in students if s['id'] == student_id), None)
    if student is None:
        await call.answer('Студент не найден', show_alert=True)
        return
    await state.update_data(selected_student=student)
    text = (
        f"🆔 {student['id']}\n"
        f"👤 {student['last_name']} {student['first_name']}\n"
        f"🎂 {student['birth_date']}\n"
        f"📚 Статус: {student['status']}\n"
        f"✉️  {student.get('email', '—')}\n"
        f"📈 GPA: {student['gpa']}"
    )

    await call.message.edit_text(
        text,
        reply_markup=builders.student_edit_kb()
    )


@edit_student_router.callback_query(F.data == 'patch_student')
async def _(call: types.CallbackQuery, state: FSMContext):
    """Редактирование студента.
    Обрабатывает выбор конкретного студента по ID.
    Выводит информацию о студенте и кнопки для редактирования."""
    data = await state.get_data()
    student = data.get('selected_student')
    await call.message.edit_text(
        texts.editing_student_msg.format(
            last_name=student['last_name'],
            first_name=student['first_name']
        ),
        reply_markup=builders.patch_student_kb()
    )


@edit_student_router.callback_query(F.data.startswith('patch-student-'))
async def _(call: types.CallbackQuery, state: FSMContext):
    """Редактирование студента.
    Выводит информацию о выбранном поле редактирования и переход к вводу
    Устанавливает state 'editing_student_setting_value'."""
    field = call.data.split('-')[-1]
    await state.update_data(editing_student_field=field)
    await call.message.edit_text(
        texts.editing_student_field_msg.format(field=field),
        reply_markup=None
    )
    await state.set_state('editing_student_setting_value')


@edit_student_router.message(StateFilter('editing_student_setting_value'))
async def _(message: types.Message, state: FSMContext):
    """Редактирование студента.
    Обрабатывает ввод нового значения поля редактирования.
    Обновляет значение поля в словаре student и отправляет запрос к API.
    Сбрасывает FSMContext и выводит сообщение об успешном редактировании."""

    new_value = message.text
    data = await state.get_data()
    field = data.get('editing_student_field')
    student = data.get('selected_student')

    student[field] = new_value
    student_id = student.pop('id')

    try:
        await api.edit_student(student_id, student)
        await message.answer(
            texts.succesfull_edit_msg.format(id=student_id),
            reply_markup=builders.main_menu_kb()
        )

    except Exception as e:
        logger.error(f'Ошибка при редактировании студента: {e}')
        await message.answer(
            texts.error_msg,
            reply_markup=builders.main_menu_kb()
        )

    await state.clear()


@edit_student_router.callback_query(F.data == 'delete_student')
async def _(call: types.CallbackQuery, state: FSMContext):
    """Удаление студента.
    Обрабатывает выбор кнопки удаления студента и отправляет запрос к API."""

    data = await state.get_data()
    student = data.get('selected_student')
    student_id = student.pop('id')

    try:
        await api.delete_student(student_id)
        await call.message.edit_text(
            texts.succesfull_delete_msg.format(id=student_id),
            reply_markup=builders.main_menu_kb()
        )

    except Exception as e:
        logger.error(f'Ошибка при удалении студента: {e}')
        await call.message.edit_text(
            texts.error_msg,
            reply_markup=builders.main_menu_kb()
        )

    await state.clear()
