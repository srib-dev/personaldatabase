from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class person_group_model(Base):
    __tablename__ = "person_group"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    when_joined_group: Mapped[date | None] = mapped_column(Date, nullable=True)
