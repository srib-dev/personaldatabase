from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base



class user_model(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    verv_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)