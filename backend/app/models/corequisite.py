# app/models/corequisite.py
import enum
from sqlalchemy import ForeignKey, Enum, Text
from sqlalchemy.orm import mapped_column, Mapped
from app.models.base import Base


class CorequisiteType(enum.Enum):
    LECTURE = "lecture"
    LAB = "lab"
    SEMINAR = "seminar"


class CorequisiteORM(Base):
    __tablename__ = "corequisites"
    corequisite_id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int | None] = mapped_column(
        ForeignKey("courses.course_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )
    course_code: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[CorequisiteType | None] = mapped_column(
        Enum(CorequisiteType, name="corequisite_type"), nullable=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    credits: Mapped[int] = mapped_column(default=1)
