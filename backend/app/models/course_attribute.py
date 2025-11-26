# app/models/course_attribute.py
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class CourseAttributeORM(Base):
    __tablename__ = "course_attributes"

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id", onupdate='CASCADE', ondelete="CASCADE"),
        primary_key=True
    )
    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("attributes.attribute_id", onupdate='CASCADE', ondelete="CASCADE"),
        primary_key=True
    )

    def __repr__(self) -> str:
        return f"CourseAttribute(course_id={self.course_id}, attribute_id={self.attribute_id})"
