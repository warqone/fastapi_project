from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards import layouts


def main_menu_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.MAIN_MENU_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def show_students_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.SHOW_STUDENTS_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def edit_student_kb(students):
    kb = InlineKeyboardBuilder()
    for student in students:
        id = student['id']
        first_name = student['first_name']
        last_name = student['last_name']
        text = f'{first_name} {last_name}'
        kb.button(text=text, callback_data=f'edit_student_{id}')
    kb.button(text='⬅️ Назад', callback_data='show_students')
    kb.adjust(1)
    return kb.as_markup()


def show_students_filters_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.SHOW_STUDENTS_FILTERS_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def student_status_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.STUDENT_STATUS_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def student_edit_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.STUDENT_EDIT_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.button(text='⬅️ Назад', callback_data='show_students')
    kb.adjust(1)
    return kb.as_markup()


def patch_student_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.PATCH_STUDENT_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.button(text='⬅️ Назад', callback_data='show_students')
    kb.adjust(1)
    return kb.as_markup()


def select_student_status_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.SELECT_STUDENT_STATUS_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def select_filter_to_delete_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.SELECT_FILTER_TO_DELETE_BUTTONS:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def select_gpa_to_delete_kb():
    kb = InlineKeyboardBuilder()
    for text, callback in layouts.SELECT_GPA_TO_DELETE:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
