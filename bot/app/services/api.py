import logging
import asyncio

import aiohttp
from aiohttp import ClientError, ClientResponseError
from typing import Optional

from config import API_URL

logger = logging.getLogger(__name__)
timeout = aiohttp.ClientTimeout(total=10)


async def fetch_students(
    page: int = 1,
    status: Optional[str] = None,
    min_gpa: Optional[int] = None,
    max_gpa: Optional[int] = None,
):
    """Асинхронный запрос к API для получения списка студентов."""

    if page < 1:
        raise ValueError("Параметр 'page' должен быть >= 1")
    if min_gpa is not None and not (0 <= min_gpa <= 100):
        raise ValueError("min_gpa должен быть от 0 до 100")
    if max_gpa is not None and not (0 <= max_gpa <= 100):
        raise ValueError("max_gpa должен быть от 0 до 100")

    params = {
        "page": page,
        "size": 20,
        "status": status,
        "min_gpa": min_gpa,
        "max_gpa": max_gpa,
    }
    params = {k: v for k, v in params.items() if v is not None}

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{API_URL}/students/", params=params) as r:
                r.raise_for_status()
                data = await r.json()
                return data.get("items", [])
    except ClientResponseError as e:
        logger.error(f'Ошибка ответа от API: {e.status} - {e.message}')
    except ClientError as e:
        logger.error(f'Сетевая ошибка при запросе: {e}')
    except asyncio.TimeoutError:
        logger.error('Таймаут при подключении к API')
    return []


async def edit_student(student_id: int, data: dict):
    """Делает запросы в API для редактирования студента."""
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.put(
                f'{API_URL}/students/{student_id}', json=data) as r:
            r.raise_for_status()
            return await r.json()


async def delete_student(student_id: int):
    """Делает запросы в API для удаления студента."""
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.delete(f'{API_URL}/students/{student_id}') as r:
            r.raise_for_status()
            return await r.json()


async def create_student(data: dict):
    """Делает запросы в API для создания студента."""
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(f'{API_URL}/students/', json=data) as r:
            r.raise_for_status()
            return await r.json()


if __name__ == "__main__":
    students = asyncio.run(fetch_students())
    print(students)
