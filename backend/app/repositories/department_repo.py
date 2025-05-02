from fastapi import HTTPException
from sqlalchemy import String, cast
from sqlalchemy.orm import Session, aliased
from app.models import Course, Department, CourseAttribute, Attribute, CoursePrerequisite


class DepartmentRepository:

    @staticmethod
    def get_departments(db: Session):
        results = (
            db.query(
                Department.prefix.label('prefix'),
                Department.name.label('name'),
            ).select_from(Department)
            .all()
        )
        return [row._asdict() for row in results]
