from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_model import PersonModel
    from personaldatabase.models.course_model import CourseModel


class PersonCourseModel(Base):
    __tablename__ = "person_courses"
    
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    course_date: Mapped[date] = mapped_column(Date, nullable=False)

    person: Mapped["PersonModel"] = relationship(back_populates="courses")
    course: Mapped["CourseModel"] = relationship(back_populates="persons")