from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class user_model(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verv_id: Mapped[int] = mapped_column(ForeignKey("verv.id"), nullable=False)
