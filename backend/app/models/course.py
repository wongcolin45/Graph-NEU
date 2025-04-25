from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Course(Base):
    __tablename__ = "courses"

    course_id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments_id", onupdate='CASCADE', ondelete="CASCADE")
    )
    course_code: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    credits: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Course(id={self.course_id}, name={self.name}, description: {self.description}, credits: {self.credits})"
