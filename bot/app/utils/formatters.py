from app.texts import texts


async def show_students(students):
    message = ''
    for student in students:
        try:
            id = student.get('id')
            first_name = student.get('first_name')
            last_name = student.get('last_name')
            status = student.get('status')
            message += (
                f'<b>{id}.</b> {first_name} {last_name} <i>({status})</i>\n'
            )
        except KeyError:
            message += texts.no_students_msg

    return message
