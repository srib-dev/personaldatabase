from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from personaldatabase.database.session import Base

if TYPE_CHECKING:
    from personaldatabase.models.person_verv_model import PersonVervModel


class VervModel(Base):
    __tablename__ = "verv"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    verv_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)

    persons: Mapped[list["PersonVervModel"]] = relationship(back_populates="verv")

