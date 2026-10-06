from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_group_model import PersonGroupModel


class GroupModel(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    group_name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    group_created_date: Mapped[date] = mapped_column(Date, nullable=False)

    members: Mapped[list["PersonGroupModel"]] = relationship(back_populates="group")
