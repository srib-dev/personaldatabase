from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_course_model import PersonCourseModel
    from personaldatabase.models.person_group_model import PersonGroupModel
    from personaldatabase.models.person_program_model import PersonProgramModel
    from personaldatabase.models.person_verv_model import PersonVervModel


class PersonModel(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    school: Mapped[str] = mapped_column(String(100), nullable=False)
    last_signed_contract: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    postbox: Mapped[str] = mapped_column(String(20), nullable=False)
    street_name: Mapped[str] = mapped_column(String(255), nullable=False)
    student_card_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    picture: Mapped[str] = mapped_column(String(512), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(
        String(255), nullable=True)

    #cascade "all, delete-orphan" sletter oppføringer i koblingstabellen om person blir slettet
    courses: Mapped[list["PersonCourseModel"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan"
    )
    groups: Mapped[list["PersonGroupModel"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan"
    )
    verv: Mapped[list["PersonVervModel"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan"
    )
    programs: Mapped[list["PersonProgramModel"]] = relationship(
        back_populates="person",
        cascade="all, delete-orphan"
    )
