from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


# CREATE TABLE course_attributes (
#     course_id INT NOT NULL,
# attribute_id INT NOT NULL,
# FOREIGN KEY (course_id) REFERENCES courses(course_id)
# ON UPDATE CASCADE ON DELETE CASCADE,
# FOREIGN KEY (attribute_id) REFERENCES attributes(attribute_id)
# ON UPDATE CASCADE ON DELETE CASCADE
# );



class CourseAttribute(Base):
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
