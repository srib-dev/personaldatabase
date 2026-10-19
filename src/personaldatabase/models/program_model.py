from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.group_model import GroupModel
    from personaldatabase.models.person_program_model import PersonProgramModel


class ProgramModel(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    program_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)

    group: Mapped["GroupModel"] = relationship(back_populates="programs")
    members: Mapped[list["PersonProgramModel"]] = relationship(
        back_populates="program", cascade="all, delete-orphan"
    )
