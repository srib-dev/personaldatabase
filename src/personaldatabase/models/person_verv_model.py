from personaldatabase.database.session import Base
from personaldatabase.models import person_model, verv_model
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class person_verv_model(Base):
    __tablename__ = "person_verv"

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"), primary_key=True)
    verv_id: Mapped[int] = mapped_column(ForeignKey("verv.id"), primary_key=True)


    person: Mapped["person_model"] = relationship(back_populates="verv")
    verv: Mapped["verv_model"] = relationship(back_populates="persons")

