import logging

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


import models
import schemas

logger = logging.getLogger(__name__)


async def create_student(db: AsyncSession, data: schemas.StudentCreate):
    """Создание нового студента в БД."""
    db_student = models.Student(**data.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    logger.info(
        f'Студент {db_student.first_name} {db_student.last_name} создан с '
        f'ID {db_student.id}'
    )
    return db_student


async def get_student(db: AsyncSession, student_id: int):
    """Получение студента по ID."""
    result = await db.execute(
        select(models.Student).filter(models.Student.id == student_id)
    )
    return result.scalars().first()


async def get_students(
    db: AsyncSession,
    status: str = None,
    min_gpa: int = None,
    max_gpa: int = None
):
    """Получение списка студентов с фильтрами и пагинацией."""
    query = select(models.Student)

    if status:
        query = query.filter(models.Student.status == status)
    if min_gpa is not None:
        query = query.filter(models.Student.gpa >= min_gpa)
    if max_gpa is not None:
        query = query.filter(models.Student.gpa <= max_gpa)

    result = await db.execute(query)
    return result.scalars().all()


async def update_student(
    db: AsyncSession,
    student_id: int,
    update_data
):
    """Обновление данных студента"""
    db_student = await get_student(db, student_id)
    if db_student:
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_student, key, value)
        await db.commit()
        await db.refresh(db_student)
        logger.info(
            f'Студент {db_student.first_name} {db_student.last_name} обновлен'
        )
    return db_student


async def delete_student(db: AsyncSession, student_id: int):
    """Удаление студента по ID."""
    db_student = await get_student(db, student_id)
    if db_student:
        await db.delete(db_student)
        await db.commit()
        logger.info(
            f'Студент {db_student.first_name} {db_student.last_name} удален'
        )
        return True
    return False


async def delete_students_by_filter(
    db: AsyncSession,
    status: str = None,
    min_gpa: int = None,
    max_gpa: int = None
):
    """Удаление студентов по фильтрам."""
    query = delete(models.Student)
    if status:
        query = query.where(models.Student.status == status)
    if min_gpa is not None:
        query = query.where(models.Student.gpa >= min_gpa)
    if max_gpa is not None:
        query = query.where(models.Student.gpa <= max_gpa)

    result = await db.execute(query)
    await db.commit()
    deleted_count = result.rowcount
    logger.info(f'Удалено студентов: {deleted_count}')
    return deleted_count
