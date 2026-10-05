from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class person_course_model(Base):
    __tablename__ = "person_courses"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    course_date: Mapped[date] = mapped_column(Date, nullable=False)