from fastapi import HTTPException
from sqlalchemy import String, Integer, cast, select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from app.CourseFilter import CourseFilter
from app.models import Course, Department, CourseAttribute, Attribute, CoursePrerequisite


default_filter = CourseFilter(0, 8000, [])


class CourseRepository:

    # ==============================================================
    # GET THE COURSE NAME AND DESCRIPTION
    # ==============================================================
    @staticmethod
    async def get_course_details(db: AsyncSession, course: str, course_filter: CourseFilter = default_filter):
        filters = [
            (Department.prefix + cast(Course.course_code, String)) == course,
            cast(Course.course_code, Integer) >= course_filter.min_course_code,
            cast(Course.course_code, Integer) <= course_filter.max_course_code,
        ]
        if course_filter.has_departments():
            filters.append(Department.prefix.in_(course_filter.get_departments()))

        stmt = (
            select(
                (Department.prefix + cast(Course.course_code, String)).label("course"),
                Course.name.label("name"),
                Course.description.label("description"),
                Course.credits.label("credits"),
            )
            .join(Department, Department.department_id == Course.department_id)
            .where(*filters)
        )

        result = await db.execute(stmt)
        row = result.first()
        return dict(row._mapping) if row else None

    # ==============================================================
    # GET LIST OF NU PATH ATTRIBUTES
    # ==============================================================
    @staticmethod
    async def get_course_attributes(db: AsyncSession, course: str, course_filter: CourseFilter = default_filter):
        stmt = (
            select(Attribute.tag)
            .select_from(Attribute)
            .join(CourseAttribute, CourseAttribute.attribute_id == Attribute.attribute_id)
            .join(Course, Course.course_id == CourseAttribute.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .where(Department.prefix + cast(Course.course_code, String) == course)
        )

        result = await db.execute(stmt)
        tags = result.scalars().all()  # list[str]

        if not course_filter.check_attributes(tags):
            return None
        return tags

    # ==============================================================
    # GET PREREQUISITES GROUPS
    # ==============================================================
    @staticmethod
    async def get_course_prerequisite_groups(db: AsyncSession, course: str):
        P = aliased(Course)     # Prerequisite
        PD = aliased(Department)  # Prerequisite Department

        stmt = (
            select(
                (PD.prefix + cast(P.course_code, String)).label("course"),
                CoursePrerequisite.group_number.label("group"),
            )
            .select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .where(Department.prefix + cast(Course.course_code, String) == course)
            .order_by(CoursePrerequisite.group_number)
        )

        result = await db.execute(stmt)
        rows = result.all()

        groups: list[list[str]] = []
        current_group = None
        for row in rows:
            course_code = row._mapping["course"]
            group_number = row._mapping["group"]
            if group_number != current_group:
                groups.append([])
                current_group = group_number
            groups[-1].append(course_code)

        return groups

    # ==============================================================
    # GET PREREQUISITES AS LIST OF COURSE CODES
    # ==============================================================
    @staticmethod
    async def get_course_prerequisites(db: AsyncSession, course: str, course_filter: CourseFilter = default_filter):
        P = aliased(Course)      # Prerequisite
        PD = aliased(Department) # Prerequisite Department

        filters = [
            (Department.prefix + cast(Course.course_code, String)) == course,
            cast(P.course_code, Integer) >= course_filter.min_course_code,
            cast(P.course_code, Integer) <= course_filter.max_course_code,
        ]
        if course_filter.has_departments():
            filters.append(PD.prefix.in_(course_filter.get_departments()))

        stmt = (
            select((PD.prefix + cast(P.course_code, String)).label("course"))
            .select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .where(*filters)
        )

        result = await db.execute(stmt)
        return [row._mapping["course"] for row in result.all()]

    # ==============================================================
    # GET NEXT COURSES AS LIST OF COURSE CODES
    # ==============================================================
    @staticmethod
    async def get_next_courses(db: AsyncSession, course: str, course_filter: CourseFilter = default_filter):
        P = aliased(Course)       # Prerequisite
        PD = aliased(Department)  # Prerequisite Department

        filters = [
            (PD.prefix + cast(P.course_code, String)) == course,
            cast(P.course_code, Integer) >= course_filter.min_course_code,
            cast(P.course_code, Integer) <= course_filter.max_course_code,
        ]
        if course_filter.has_departments():
            filters.append(PD.prefix.in_(course_filter.get_departments()))

        stmt = (
            select((Department.prefix + cast(Course.course_code, String)).label("course"))
            .select_from(CoursePrerequisite)
            .join(Course, Course.course_id == CoursePrerequisite.course_id)
            .join(Department, Department.department_id == Course.department_id)
            .join(P, P.course_id == CoursePrerequisite.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .where(*filters)
        )

        result = await db.execute(stmt)
        # Deduplicate while preserving order
        seen = set()
        clean_results = []
        for row in result.all():
            code = row._mapping["course"]
            if code not in seen:
                seen.add(code)
                clean_results.append(code)
        return clean_results

    # ==============================================================
    # GET ALL COURSES
    # ==============================================================
    @staticmethod
    async def get_all_courses(db: AsyncSession):
        stmt = (
            select(
                (Department.prefix + cast(Course.course_code, String)).label("course"),
                Course.name.label("name"),
            )
            .join(Department, Department.department_id == Course.department_id)
        )
        result = await db.execute(stmt)
        return [dict(row._mapping) for row in result.all()]

    # ==============================================================
    # GET COURSES SIMILAR TO COURSE
    # ==============================================================
    @staticmethod
    async def get_courses_like(db: AsyncSession, course: str):
        # Use ILIKE for case-insensitive match
        query = f"%{course.upper()}%"
        stmt = (
            select(
                (Department.prefix + cast(Course.course_code, String)).label("course"),
                Course.name.label("name"),
            )
            .select_from(Course)
            .join(Department, Department.department_id == Course.department_id)
            .where((Department.prefix + cast(Course.course_code, String)).ilike(query))
        )
        result = await db.execute(stmt)
        return [dict(row._mapping) for row in result.all()]
