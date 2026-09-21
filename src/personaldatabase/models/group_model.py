from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class group_model(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    group_name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    group_created_date: Mapped[date] = mapped_column(Date, nullable=False)
