from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class person_model(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    school: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_signed_contract: Mapped[date | None] = mapped_column(Date, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    postbox: Mapped[str | None] = mapped_column(String(20), nullable=True)
    street_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    student_card_number: Mapped[str | None] = mapped_column(String(50), nullable=False)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    birthdate: Mapped[date | None] = mapped_column(Date, nullable=False)
    picture: Mapped[str | None] = mapped_column(String(512), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(50), nullable=True)
