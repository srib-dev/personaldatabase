from datetime import date
from sqlalchemy.orm import relationship
from personaldatabase.models import person_model
from personaldatabase.models import group_model
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class person_group_model(Base):
    __tablename__ = "person_groups"

    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    when_joined_group: Mapped[date] = mapped_column(Date, nullable=False)

    person: Mapped["person_model"] = relationship(back_populates="groups")
    group: Mapped["group_model"] = relationship(back_populates="members")
