# app/repositories/course_repository.py
from sqlalchemy import String, Integer, cast, select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from app.CourseFilter import CourseFilter
from app.models import CourseORM, DepartmentORM, CourseAttributeORM, AttributeORM, CoursePrerequisiteORM

default_filter = CourseFilter(0, 8000, [])

class CourseRepository:
    """Interface for interacting with courses in database"""

    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_course_details(self, course: str, course_filter: CourseFilter = default_filter) -> dict | None:
        filters = [
            (DepartmentORM.prefix + cast(CourseORM.course_code, String)) == course,
            cast(CourseORM.course_code, Integer) >= course_filter.min_course_code,
            cast(CourseORM.course_code, Integer) <= course_filter.max_course_code,
        ]
        if course_filter.has_departments():
            filters.append(DepartmentORM.prefix.in_(course_filter.get_departments()))

        query = (
            select(
                (DepartmentORM.prefix + cast(CourseORM.course_code, String)).label("course"),
                CourseORM.name.label("name"),
                CourseORM.description.label("description"),
                CourseORM.credits.label("credits"),
            )
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
            .where(*filters)
        )

        result = await self.db.execute(query)
        row = result.first()
        return dict(row._mapping) if row else None


    async def get_course_attributes(self, course: str, course_filter: CourseFilter = default_filter):
        query = (
            select(AttributeORM.tag)
            .select_from(AttributeORM)
            .join(CourseAttributeORM, CourseAttributeORM.attribute_id == AttributeORM.attribute_id)
            .join(CourseORM, CourseORM.course_id == CourseAttributeORM.course_id)
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
            .where(DepartmentORM.prefix + cast(CourseORM.course_code, String) == course)
        )

        result = await self.db.execute(query)
        tags = result.scalars().all()

        if not course_filter.check_attributes(tags):
            return None
        return tags


    async def get_course_prerequisite_groups(self, course: str):
        P = aliased(CourseORM)     # Prerequisite
        PD = aliased(DepartmentORM)  # Prerequisite Department
        query = (
            select(
                (PD.prefix + cast(P.course_code, String)).label("course"),
                CoursePrerequisiteORM.group_number.label("group"),
            )
            .select_from(CoursePrerequisiteORM)
            .join(CourseORM, CourseORM.course_id == CoursePrerequisiteORM.course_id)
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
            .join(P, P.course_id == CoursePrerequisiteORM.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .where(DepartmentORM.prefix + cast(CourseORM.course_code, String) == course)
            .order_by(CoursePrerequisiteORM.group_number)
        )
        result = await self.db.execute(query)
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


    async def get_course_prerequisites(self, course: str, course_filter: CourseFilter = default_filter):
        P = aliased(CourseORM)      # Prerequisite
        PD = aliased(DepartmentORM) # Prerequisite Department

        filters = [
            (DepartmentORM.prefix + cast(CourseORM.course_code, String)) == course,
            cast(P.course_code, Integer) >= course_filter.min_course_code,
            cast(P.course_code, Integer) <= course_filter.max_course_code,
        ]
        if course_filter.has_departments():
            filters.append(PD.prefix.in_(course_filter.get_departments()))

        stmt = (
            select((PD.prefix + cast(P.course_code, String)).label("course"))
            .select_from(CoursePrerequisiteORM)
            .join(CourseORM, CourseORM.course_id == CoursePrerequisiteORM.course_id)
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
            .join(P, P.course_id == CoursePrerequisiteORM.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .where(*filters)
        )

        result = await self.db.execute(stmt)
        return [row._mapping["course"] for row in result.all()]


    async def get_next_courses(self, course: str, course_filter: CourseFilter = default_filter) -> dict:
        P = aliased(CourseORM)       # Prerequisite
        PD = aliased(DepartmentORM)  # Prerequisite Department

        filters = [
            (PD.prefix + cast(P.course_code, String)) == course,
            cast(P.course_code, Integer) >= course_filter.min_course_code,
            cast(P.course_code, Integer) <= course_filter.max_course_code,
        ]
        if course_filter.has_departments():
            filters.append(PD.prefix.in_(course_filter.get_departments()))

        query = (
            select((DepartmentORM.prefix + cast(CourseORM.course_code, String)).label("course"))
            .select_from(CoursePrerequisiteORM)
            .join(CourseORM, CourseORM.course_id == CoursePrerequisiteORM.course_id)
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
            .join(P, P.course_id == CoursePrerequisiteORM.prerequisite_id)
            .join(PD, PD.department_id == P.department_id)
            .where(*filters)
        )

        result = await self.db.execute(query)
        # Deduplicate while preserving order
        seen = set()
        clean_results = []
        for row in result.all():
            code = row._mapping["course"]
            if code not in seen:
                seen.add(code)
                clean_results.append(code)
        return clean_results


    async def get_all_courses(self) -> list[dict]:
        query = (
            select(
                (DepartmentORM.prefix + cast(CourseORM.course_code, String)).label("course"),
                CourseORM.name.label("name"),
            )
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
        )
        result = await self.db.execute(query)
        return [dict(row._mapping) for row in result.all()]


    async def get_courses_like(self, search_query: str) -> list[dict]:
        query = (
            select(
                (DepartmentORM.prefix + cast(CourseORM.course_code, String)).label("course"),
                CourseORM.name.label("name"),
            )
            .select_from(CourseORM)
            .join(DepartmentORM, DepartmentORM.department_id == CourseORM.department_id)
            .where((DepartmentORM.prefix + cast(CourseORM.course_code, String) + CourseORM.name).ilike(f"%{search_query}%"))
        )
        result = await self.db.execute(query)
        return [dict(row._mapping) for row in result.all()]
