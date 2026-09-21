from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class verv_model(Base):
    __tablename__ = "verv"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    verv_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
