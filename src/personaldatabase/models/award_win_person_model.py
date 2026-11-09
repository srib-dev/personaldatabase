from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.award_win_model import AwardWinModel
    from personaldatabase.models.person_model import PersonModel


class AwardWinPersonModel(Base):
    __tablename__ = "award_win_persons"

    award_win_id: Mapped[int] = mapped_column(
        ForeignKey("award_wins.id"), primary_key=True
    )
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"), primary_key=True
    )

    award_win: Mapped["AwardWinModel"] = relationship(back_populates="persons")
    person: Mapped["PersonModel"] = relationship(back_populates="award_wins")
