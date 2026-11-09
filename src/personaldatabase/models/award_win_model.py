from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.award_model import AwardModel
    from personaldatabase.models.award_win_person_model import AwardWinPersonModel
    from personaldatabase.models.person_model import PersonModel
    from personaldatabase.models.program_model import ProgramModel


class AwardWinModel(Base):
    __tablename__ = "award_wins"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    award_id: Mapped[int] = mapped_column(ForeignKey("awards.id"), nullable=False)
    semester: Mapped[str] = mapped_column(String(20), nullable=False)
    program_id: Mapped[int | None] = mapped_column(
        ForeignKey("programs.id"), nullable=True
    )
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)

    award: Mapped["AwardModel"] = relationship(back_populates="wins")
    program: Mapped["ProgramModel | None"] = relationship(back_populates="award_wins")
    persons: Mapped[list["AwardWinPersonModel"]] = relationship(
        back_populates="award_win", cascade="all, delete-orphan"
    )

    @property
    def winners(self) -> list["PersonModel"]:
        return [awp.person for awp in self.persons if awp.person is not None]
