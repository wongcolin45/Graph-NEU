from fastapi import HTTPException
from sqlalchemy import String, cast
from sqlalchemy.orm import Session, aliased
from app.models import Course, Department, CourseAttribute, Attribute, CoursePrerequisite


class CourseRepository:

    @staticmethod
    def get_course_details(db: Session, course):
        result = (
            db.query(
                (Department.prefix + ' ' + Course.course_code.cast(String)).label("course"),
                Course.name.label("name"),
                Course.description.label("description"),
                Course.credits.label("credits")
            )
              .join(Department, Department.department_id == Course.department_id)
              .filter(
                  Department.prefix + Course.course_code.cast(String) == course,
              )
              .first()
        )
        if not result:
            return None
        return result._asdict()

    @staticmethod
    def get_course_attributes(db: Session, course):
        results = (
            db.query(Attribute.tag)
            .join(CourseAttribute, CourseAttribute.attribute_id == Attribute.attribute_id)
            .join(Course, Course.course_id == CourseAttribute.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .filter(
                Department.prefix + Course.course_code.cast(String) == course
            )
            .all()
        )
        for i in range(len(results)):
            results[i] = results[i][0]
        return results

    @staticmethod
    def get_course_prerequisite_groups(db: Session, course):
        P = aliased(Course)  # Prerequisite
        PD = aliased(Department)  # Prerequisite Department
        results = (
            db.query(
                (PD.prefix + cast(P.course_code, String)).label('course'),
                CoursePrerequisite.group_number.label('group'),
            ).select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .filter(
                Department.prefix + cast(Course.course_code, String) == course
            )
            .order_by(CoursePrerequisite.group_number)
            .all()
        )

        groups = []
        current_group = 0
        for result in results:
            group_number = result[1]
            course = result[0]
            if group_number != current_group:
                groups.append([])
                current_group += 1
            groups[-1].append(course)

        return groups

    @staticmethod
    def get_course_prerequisites(db: Session, course):
        P = aliased(Course)      # Prerequisite
        PD = aliased(Department) # Prerequisite Department
        results = (
            db.query(
                (PD.prefix + cast(P.course_code, String)).label("course")
            ).select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .filter(
                Department.prefix + cast(Course.course_code,String) == course,
            )
            .all()
        )
        clean_results = []
        for result in results:
            clean_results.append(result[0])
        return clean_results

    @staticmethod
    def get_next_courses(db: Session, course):
        P = aliased(Course)       # Prerequisite
        PD = aliased(Department)  # Prerequisite Department
        results = (
            db.query(
                (Department.prefix + cast(Course.course_code, String)).label("course")
            ).select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .filter(
                PD.prefix + cast(P.course_code, String) == course
            )
            .all()
        )
        clean_results = []
        for result in results:
            if result[0] in clean_results:
                continue
            clean_results.append(result[0])
        return clean_results

    @staticmethod
    def get_course_data(db: Session, course):
        attributes = CourseRepository.get_course_attributes(db, course)
        info = CourseRepository.get_course_details(db, course)

        if info is None:
            raise HTTPException(status_code=404, detail=f'{course} not found')

        info['attributes'] = attributes
        info['prerequisites'] = CourseRepository.get_course_prerequisites(db, course)
        return info

    @staticmethod
    def get_all_courses(db: Session):
        results = (
            db.query(
                (Department.prefix + Course.course_code.cast(String)).label("course"),
                Course.name.label("name"),
            )
            .join(Department, Department.department_id == Course.department_id)
            .all()
        )
        clean_results = []
        for result in results:
            clean_results.append(result._asdict())
        return clean_results
