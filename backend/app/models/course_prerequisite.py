from sqlalchemy import ForeignKey, Text, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


# CREATE TABLE course_prerequisites(
#     course_id INT NOT NULL,
# prerequisite_id INT NOT NULL,
# PRIMARY KEY(course_id, prerequisite_id),
# FOREIGN KEY (course_id) REFERENCES courses(course_id)
# ON UPDATE CASCADE
# ON DELETE CASCADE,
# FOREIGN KEY (prerequisite_id) REFERENCES courses(course_id)
# ON UPDATE CASCADE
# ON DELETE CASCADE
# );



class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id", onupdate='CASCADE', ondelete="CASCADE"),
        primary_key=True
    )
    prerequisite_id: Mapped[int] = mapped_column(
        ForeignKey("courses.course_id", onupdate='CASCADE', ondelete="CASCADE"),
        primary_key=True
    )

    __table_args__ = (
        PrimaryKeyConstraint("course_id", "prerequisite_id"),
    )

    def __repr__(self) -> str:
        return f"CoursePrerequisite(course_id={self.course_id}, prerequisite_id={self.prerequisite_id})"
