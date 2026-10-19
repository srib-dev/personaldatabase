from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_model import PersonModel
    from personaldatabase.models.program_model import ProgramModel


class PersonProgramModel(Base):
    __tablename__ = "person_programs"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"), primary_key=True)
    program_role: Mapped[str] = mapped_column(String(100), nullable=False)

    person: Mapped["PersonModel"] = relationship(back_populates="programs")
    program: Mapped["ProgramModel"] = relationship(back_populates="members")
