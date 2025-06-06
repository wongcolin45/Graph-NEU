from fastapi import HTTPException
from sqlalchemy import String, cast, Integer
from sqlalchemy.orm import Session, aliased

from app.CourseFilter import CourseFilter
from app.models import Course, Department, CourseAttribute, Attribute, CoursePrerequisite


default_filter = CourseFilter(0, 8000, [])

class CourseRepository:

    # ==============================================================
    # GET THE COURSE NAME AND DESCRIPTION
    # ==============================================================
    @staticmethod
    def get_course_details(db: Session, course, course_filter: CourseFilter = default_filter):

        filters = [
            (Department.prefix + cast(Course.course_code, String)) == course,
            (cast(Course.course_code, Integer)) >= course_filter.min_course_code,
            (cast(Course.course_code, Integer)) <= course_filter.max_course_code
        ]

        if course_filter.has_departments():
            filters.append(Department.prefix.in_(course_filter.get_departments()))

        result = (
            db.query(
                (Department.prefix + ' ' + Course.course_code.cast(String)).label("course"),
                Course.name.label("name"),
                Course.description.label("description"),
                Course.credits.label("credits")
            )
              .join(Department, Department.department_id == Course.department_id)
              .filter(*filters)
              .first()
        )
        if not result:
            return None
        return result._asdict()

    # ==============================================================
    # GET LIST OF NU PATH ATTRIBUTES
    # ==============================================================
    @staticmethod
    def get_course_attributes(db: Session, course, course_filter: CourseFilter = default_filter):
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

        if not course_filter.check_attributes(results):
            return None

        return results

    # ==============================================================
    # GET PREREQUISITES GROUPS
    # ==============================================================
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

    # ==============================================================
    # GET PREREQUISITES AS LIST OF COURSE CODES
    # ==============================================================
    @staticmethod
    def get_course_prerequisites(db: Session, course, course_filter: CourseFilter = default_filter):
        P = aliased(Course)      # Prerequisite
        PD = aliased(Department) # Prerequisite Department

        filters = [
            (Department.prefix + cast(Course.course_code,String)) == course,
            (cast(P.course_code, Integer)) >= course_filter.min_course_code,
            (cast(P.course_code, Integer)) <= course_filter.max_course_code
        ]

        if course_filter.has_departments():
            filters.append(PD.prefix.in_(course_filter.get_departments()))

        results = (
            db.query(
                (PD.prefix + cast(P.course_code, String)).label("course")
            ).select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .filter(*filters)
            .all()
        )
        clean_results = []
        for result in results:
            clean_results.append(result[0])
        return clean_results

    # ==============================================================
    # GET NEXT COURSES AS LIST OF COURSE CODES
    # ==============================================================
    @staticmethod
    def get_next_courses(db: Session, course, course_filter: CourseFilter = default_filter):
        P = aliased(Course)       # Prerequisite
        PD = aliased(Department)  # Prerequisite Department

        filters = [
            (PD.prefix + cast(P.course_code, String)) == course,
            (cast(P.course_code, Integer)) >= course_filter.min_course_code,
            (cast(P.course_code, Integer)) <= course_filter.max_course_code
        ]

        if course_filter.has_departments():
            filters.append(PD.prefix.in_(course_filter.get_departments()))

        results = (
            db.query(
                (Department.prefix + cast(Course.course_code, String)).label("course")
            ).select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .filter(*filters)
            .all()
        )
        clean_results = []
        for result in results:
            if result[0] in clean_results:
                continue
            clean_results.append(result[0])
        return clean_results

    # ==============================================================
    # GET ALL COURSES
    # ==============================================================
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

    # ==============================================================
    # GET COURSES SIMILAR TO COURSE
    # ==============================================================
    @staticmethod
    def get_courses_like(db: Session, course):
        query = f"%{course.upper()}%"
        results = (db.query(
                    (Department.prefix + cast(Course.course_code, String)).label("course"),
                     Course.name.label('name')
                    ).select_from(Course)
                   .join(Department, Department.department_id == Course.department_id)
                   .all())
        return results