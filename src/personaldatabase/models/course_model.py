from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from personaldatabase.database.session import Base


class course_model(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False)
    course_provider: Mapped[str] = mapped_column(String(100), nullable=False)
