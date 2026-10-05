from datetime import date
from personaldatabase.models import person_group_model
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base


class group_model(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    group_name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    group_created_date: Mapped[date] = mapped_column(Date, nullable=False)

    members: Mapped[list["person_group_model"]] = relationship(back_populates="group")