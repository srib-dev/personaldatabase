from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.award_win_model import AwardWinModel


class AwardModel(Base):
    __tablename__ = "awards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    award_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_program_award: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    wins: Mapped[list["AwardWinModel"]] = relationship(
        back_populates="award", cascade="all, delete-orphan"
    )
