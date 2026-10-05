from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_model import PersonModel
    from personaldatabase.models.group_model import GroupModel


class PersonGroupModel(Base):
    __tablename__ = "person_groups"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    when_joined_group: Mapped[date] = mapped_column(Date, nullable=False)

    person: Mapped["PersonModel"] = relationship(back_populates="groups")
    group: Mapped["GroupModel"] = relationship(back_populates="members")

