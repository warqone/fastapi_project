from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional


class StudentBase(BaseModel):
    """Базовая схема студента."""
    first_name: str = Field(..., max_length=50, example='Иван')
    last_name: str = Field(..., max_length=50, example='Иванов')
    birth_date: date = Field(..., example='1998-07-09')
    status: str = Field(..., example="ACTIVE")
    email: Optional[EmailStr] = Field(None, example='user@gmail.com')
    gpa: Optional[int] = Field(None, ge=0, le=100, example=85)


class StudentCreate(StudentBase):
    """Схема для создания студента."""
    pass


class StudentUpdate(BaseModel):
    """Схема для обновления данных студента."""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    status: Optional[str] = None
    email: Optional[EmailStr] = None
    gpa: Optional[int] = Field(None, ge=0, le=100)


class StudentResponse(StudentBase):
    """Схема ответа с данными студента."""
    id: int

    class Config:
        from_attributes = True
