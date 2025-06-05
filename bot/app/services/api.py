import aiohttp
import asyncio
from typing import Optional

from config import API_URL


timeout = aiohttp.ClientTimeout(total=10)


async def fetch_students(
    page: int = 1,
    status: Optional[str] = None,
    min_gpa: Optional[int] = None,
    max_gpa: Optional[int] = None,
):
    """Делает запросы в API для получения списка студентов с параметрами."""
    params = {
        "page": page,
        "size": 20,
        "status": status,
        "min_gpa": min_gpa,
        "max_gpa": max_gpa,
    }
    params = {k: v for k, v in params.items() if v is not None}

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(f"{API_URL}/students/", params=params) as r:
            r.raise_for_status()
            data = await r.json()
            return data['items'] if data['items'] else 'Нет студентов'


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
