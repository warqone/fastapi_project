from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from database import AsyncSessionLocal
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router.post("/students/",
             response_model=schemas.StudentResponse,
             summary='Создание нового студента',
             status_code=HTTPStatus.CREATED)
async def create_student(
    student: schemas.StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создание нового студента."""
    try:
        logger.info(f'Создание нового студента: {student}')
        return await crud.create_student(db, student)

    except Exception as e:
        logger.error(f'Ошибка при создании студента: {e}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/students/{student_id}",
            response_model=schemas.StudentResponse,
            summary='Получение информации о студенте по ID')
async def read_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получение информации о студенте по ID."""
    db_student = await crud.get_student(db, student_id)

    if db_student is None:
        logger.warning(f'Студент не найден: ID {student_id}')
        raise HTTPException(status_code=404, detail='Студент не найден')

    return db_student


@router.get("/students/",
            response_model=Page[schemas.StudentResponse],
            summary='Получение списка студентов с пагинацией и фильтрами')
async def read_students(
    status: str = Query(None),
    min_gpa: int = Query(None, ge=0, le=100),
    max_gpa: int = Query(None, ge=0, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Получение списка студентов с пагинацией и фильтрами."""
    result = await crud.get_students(db, status, min_gpa, max_gpa)

    return paginate(result)


@router.put("/students/{student_id}",
            response_model=schemas.StudentResponse,
            summary='Обновление информации о студенте',
            status_code=HTTPStatus.CREATED)
async def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновление информации о студенте."""
    db_student = await crud.update_student(db, student_id, student_update)

    if db_student is None:
        logger.warning(f'Обновление студента не удалось: ID {student_id}')
        raise HTTPException(status_code=404, detail='Студент не найден')

    return db_student


@router.delete("/students/{student_id}",
               summary='Удаление студента по ID',
               status_code=HTTPStatus.NO_CONTENT)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удаление студента по ID."""
    success = await crud.delete_student(db, student_id)

    if not success:
        logger.warning(f'Удаление студента не удалось: ID {student_id}')
        raise HTTPException(status_code=404, detail='Студент не найден')

    return {'detail': 'Студент удален'}


@router.delete("/students/",
               summary='Удаление студентов по фильтрам',
               status_code=HTTPStatus.NO_CONTENT)
async def delete_students_by_filter(
    status: str = Query(None),
    min_gpa: int = Query(None, ge=0, le=100),
    max_gpa: int = Query(None, ge=0, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Удаление студентов по фильтрам (например по статусу)."""
    deleted_count = await crud.delete_students_by_filter(
        db, status, min_gpa, max_gpa
    )

    if deleted_count == 0:
        logger.info('Нет студентов для удаления по фильтрам.')
        return {'detail': 'Нет студентов для удаления по фильтрам.'}

    return {'detail': f'Удалено студентов: {deleted_count}'}
