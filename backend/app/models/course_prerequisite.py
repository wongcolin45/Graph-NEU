# app/models/course_prerequisite.py
from sqlalchemy import ForeignKey, Text, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class CoursePrerequisiteORM(Base):
    __tablename__ = "course_prerequisites"

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id", onupdate='CASCADE', ondelete="CASCADE"),
        primary_key=True
    )
    prerequisite_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id", onupdate='CASCADE', ondelete="CASCADE"),
        primary_key=True
    )
    group_number: Mapped[int] = mapped_column()

    __table_args__ = (
        PrimaryKeyConstraint("course_id", "prerequisite_id"),
    )

    def __repr__(self) -> str:
        return f"CoursePrerequisite(course_id={self.course_id}, prerequisite_id={self.prerequisite_id})"
