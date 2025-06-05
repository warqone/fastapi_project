async def show_students(students):
    message = ''
    for student in students:
        id = student['id']
        first_name = student['first_name']
        last_name = student['last_name']
        status = student['status']
        message += (
            f'<b>{id}.</b> {first_name} {last_name} <i>({status})</i>\n\n'
        )
    return message
