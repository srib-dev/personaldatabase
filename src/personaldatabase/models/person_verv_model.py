from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_model import PersonModel
    from personaldatabase.models.verv_model import VervModel


class PersonVervModel(Base):
    __tablename__ = "person_verv"

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"), primary_key=True)
    verv_id: Mapped[int] = mapped_column(ForeignKey("verv.id"), primary_key=True)

    person: Mapped["PersonModel"] = relationship(back_populates="verv")
    verv: Mapped["VervModel"] = relationship(back_populates="persons")


