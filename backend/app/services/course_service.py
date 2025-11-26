# app/services/course_service.py
from __future__ import annotations
from app.CourseFilter import CourseFilter
from app.repositories.course_repository import CourseRepository
from rapidfuzz import process, fuzz


# Default filter matches your original behavior
default_filter = CourseFilter(0, 8000, [])


class CourseService:


    def __init__(self, repository: CourseRepository):
        self.repository = repository


    async def get_course_data(
        self,
        course: str,
        course_filter = default_filter
    ) -> dict | None:
        """
        Returns a dict containing course details, attributes, and prerequisites.
        Returns None if the course is not found or filtered out.
        """
        # Expect repo functions to return already-materialized dicts/lists
        info = await self.repository.get_course_details(course, course_filter)
        if info is None:
            return None

        attributes = await self.repository.get_course_attributes(course, course_filter)
        if attributes is None:
            return None

        # Prerequisites do not use the filter (per your original logic)
        prerequisites = await self.repository.get_course_prerequisites(course)

        # Compose a plain dict payload (no ORM instances)
        info["attributes"] = attributes
        info["prerequisites"] = prerequisites or []
        return info


    async def prerequisites_met(
        self,
        course: str,
        courses_taken: list[str],
    ) -> dict:
        """
        Checks if prerequisites for `course` are met given `courses_taken`.
        Returns: {"satisfied": bool, "message": str}
        """
        # Expect a list[list[str]] where each inner list is an OR-group
        prerequisite_groups = await self.repository.get_course_prerequisite_groups(course)
        prerequisite_groups = prerequisite_groups or []

        missing: list[list[str]] = []

        for group in prerequisite_groups:
            group_missing: list[str] = []
            group_satisfied = False
            for c in group:
                if c in courses_taken:
                    group_satisfied = True
                else:
                    group_missing.append(c)

            if group_satisfied:
                missing = []
                break
            else:
                missing.append(group_missing)

        if not missing:
            return {"satisfied": True, "message": "n/a"}

        parts: list[str] = []
        for group in missing:
            if not group:
                continue
            if len(group) == 1:
                parts.append(f"Take: {group[0]};")
            else:
                parts.append("Take: " + " or ".join(group) + ";")
        return {"satisfied": False, "message": "".join(parts)}


    async def get_select_courses(
        self,
        courses: list[str],
    ) -> dict[str, dict | None]:
        """
        Fetch details for a list of courses. Sequential (no shared-session concurrency).
        Returns a mapping {course_code: course_data_or_None}
        """
        out: dict[str, dict | None] = {}
        for course in courses:
            out[course] = await self.repository.get_course_data(course)
        return out


    async def get_next_courses(
        self,
        node,
        course_filter: CourseFilter | None
   ) -> list[dict]:
        if course_filter is None:
            return await self.repository.get_next_courses(node)
        return await self.repository.get_next_courses(node, course_filter)


    async def check_select_courses(
        self,
        courses: list[str],
        courses_taken: list[str],
    ) -> dict[str, dict]:
        """
        Check prerequisites for a list of courses. Sequential (no shared-session concurrency).
        Returns a mapping {course_code: {"satisfied": bool, "message": str}}
        """
        out: dict[str, dict] = {}
        for course in courses:
            out[course] = await self.prerequisites_met(course, courses_taken)
        return out



    async def search_courses(
        self,
        query: str,
        limit: int,
    ) -> list[dict]:
        """
        Fuzzy-search course names/codes, returning a list of:
          { "course": <code>, "name": <name> }
        """
        rows = await self.repository.get_courses_like(query)
        items: dict[str, dict] = {}

        for row in rows:
            if isinstance(row, dict):
                course_code = row.get("course")
                name = row.get("name")
            else:
                course_code, name = row[0], row[1]

            if course_code is None or name is None:
                continue

            key = f"{course_code} {name}"
            items[key] = {"course": course_code, "name": name}

        # Fuzzy match against the combined "code name" key
        matches = process.extract(
            query,
            items.keys(),
            scorer=fuzz.WRatio,
            limit=limit,
        )

        out: list[dict] = []
        for matched_key, *_ in matches:
            out.append(items[matched_key])

        return out
