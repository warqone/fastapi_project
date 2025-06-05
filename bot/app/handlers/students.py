from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from app.keyboards import builders
from app.services.api import fetch_students
from app.utils.formatters import show_students
from app.texts import texts

students_router = Router()


@students_router.callback_query(F.data == 'show_students')
async def _(call: types.CallbackQuery, state: FSMContext):
    students = await fetch_students()
    if students:
        msg = await show_students(students)
    else:
        msg = texts.error_msg
    await state.update_data(students=students)
    await call.message.edit_text(msg, reply_markup=builders.show_students_kb())


@students_router.callback_query(F.data == 'show_students_edit')
async def _(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    students = data.get('students')
    await call.message.edit_reply_markup(
        reply_markup=builders.edit_student_kb(students)
    )


@students_router.callback_query(F.data == 'show_students_filters')
async def _(call: types.CallbackQuery):
    await call.message.edit_reply_markup(
        reply_markup=builders.show_students_filters_kb()
    )


@students_router.callback_query(F.data.startswith('filter_'))
async def _(call: types.CallbackQuery, state: FSMContext):
    filter_type = call.data.split('_')[1]

    if filter_type == 'status':
        msg = texts.choose_status
        markup = builders.student_status_kb()
        return await call.message.edit_text(msg, reply_markup=markup)

    elif filter_type == 'mingpa':
        msg = 'Введите минимальный средний балл (не доделано)'
        await state.set_state(filter_type)

    elif filter_type == 'maxgpa':
        msg = 'Введите максимальный средний балл (не доделано)'
        await state.set_state(filter_type)

    await call.message.answer(msg)


@students_router.callback_query(F.data.startswith('status_filter_'))
async def _(call: types.CallbackQuery):
    status = call.data.split('_')[2]
    if status == 'ACADEMIC':
        status = 'ACADEMIC_LEAVE'  # КОСТЫЛЬ
    students = await fetch_students(status=status)
    if students:
        msg = await show_students(students)
    else:
        msg = texts.error_msg
    await call.message.edit_text(msg, reply_markup=builders.show_students_kb())
