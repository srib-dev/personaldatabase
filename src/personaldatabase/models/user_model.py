from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base



class user_model(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)