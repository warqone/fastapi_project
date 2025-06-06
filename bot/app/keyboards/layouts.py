MAIN_MENU_BUTTONS = (
    ('📑 Просмотреть список студентов', 'show_students'),
    ('➕ Добавить студента', 'add_student'),
)
SHOW_STUDENTS_BUTTONS = (
    ('👨‍🎓 Выбрать студента (для редактирования)', 'show_students_edit'),
    ('⚙️ Фильтры', 'show_students_filters'),
    ('⬅️ Назад в главное меню', 'back_to_main_menu')
)
SHOW_STUDENTS_FILTERS_BUTTONS = (
    ('Выбрать статус', 'filter_status'),
    ('Минимальный средний балл', 'filter_mingpa'),
    ('Максимальный средний балл', 'filter_maxgpa')
)
STUDENT_STATUS_BUTTONS = (
    ('Активный', 'status-filter_ACTIVE'),
    ('Отчислен', 'status-filter_EXPELLED'),
    ('Академический отпуск', 'status-filter_ACADEMIC_LEAVE'),
    ('Закончил', 'status-filter_GRADUATED')
)
STUDENT_EDIT_BUTTONS = (
    ('✏️ Редактировать', 'patch_student'),
    ('🗑️ Удалить', 'delete_student'),
)
PATCH_STUDENT_BUTTONS = (
    ('Изменить имя', 'patch-student-first_name'),
    ('Изменить фамилию', 'patch-student-last_name'),
    ('Изменить дату рождения', 'patch-student-birth_date'),
    ('Изменить статус', 'patch-student-status'),
    ('Изменить средний балл', 'patch-student-gpa'),
    ('Изменить почту', 'patch-student-email')
)
SELECT_STUDENT_STATUS_BUTTONS = (
    ('Активный', 'status-ACTIVE'),
    ('Отчислен', 'status-EXPELLED'),
    ('Академический отпуск', 'status-ACADEMIC_LEAVE'),
    ('Закончил', 'status-GRADUATED')
)
SELECT_FILTER_TO_DELETE_BUTTONS = (
    ('По статусу', 'delete-by_status'),
    ('По минимальному баллу', 'delete-by_mingpa'),
    ('По максимальному баллу', 'delete-by_maxgpa')
)
SELECT_STATUS_TO_DELETE = (
    ('Активный', 'delete-status_ACTIVE'),
    ('Отчислен', 'delete-status_EXPELLED'),
    ('Академический отпуск', 'delete-status-ACADEMIC_LEAVE'),
    ('Закончил', 'delete-status_GRADUATED')
)
SELECT_GPA_TO_DELETE = (
    ('100', 'delete-gpa_100'),
    ('90', 'delete-gpa_90'),
    ('80', 'delete-gpa_80'),
    ('70', 'delete-gpa_70'),
    ('60', 'delete-gpa_60'),
    ('50', 'delete-gpa_50'),
    ('40', 'delete-gpa_40'),
    ('30', 'delete-gpa_30'),
    ('20', 'delete-gpa_20'),
    ('10', 'delete-gpa_10')
)
SELECT_STUDENT_STATUS_FILTER_BUTTONS = (
    ('Активный', 'status-filter-ACTIVE'),
    ('Отчислен', 'status-filter-EXPELLED'),
    ('Академический отпуск', 'status-filter-ACADEMIC_LEAVE'),
    ('Закончил', 'status-filter-GRADUATED')
)
