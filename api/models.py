from sqlalchemy import Column, Integer, String, Date, Enum
from database import Base
import enum


class StudentStatus(str, enum.Enum):
    """Статусы студента."""
    ACTIVE = "активный"
    EXPELLED = "отчислен"
    ACADEMIC_LEAVE = "академический отпуск"
    GRADUATED = "закончил"


class Student(Base):
    """Модель студента в базе данных."""
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)
    email = Column(String(100), unique=True, nullable=True)
    gpa = Column(Integer, nullable=True)
