# app/services/course_service.py

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from app.CourseFilter import CourseFilter
# If your repo lives at app/repositories/course_repo.py, keep this import:
from app.repositories.course_repo import CourseRepository
# If your project used a package import like "from app.repositories import CourseRepository",
# adjust accordingly.

from rapidfuzz import process, fuzz


# Default filter matches your original behavior
default_filter = CourseFilter(0, 8000, [])


class CourseService:
    """
    Service layer for course-related operations. All methods are careful to:
      - Avoid concurrent use of the same AsyncSession
      - Fully materialize repository results (dicts/lists), not ORM objects
      - Return plain dicts/lists to avoid lazy loads during response serialization
    """

    @staticmethod
    async def get_course_data(
        db: AsyncSession,
        course: str,
        course_filter: CourseFilter = default_filter,
    ) -> dict | None:
        """
        Returns a dict containing course details, attributes, and prerequisites.
        Returns None if the course is not found or filtered out.
        """
        # Expect repo functions to return already-materialized dicts/lists
        info = await CourseRepository.get_course_details(db, course, course_filter)
        if info is None:
            return None

        attributes = await CourseRepository.get_course_attributes(db, course, course_filter)
        if attributes is None:
            return None

        # Prerequisites do not use the filter (per your original logic)
        prerequisites = await CourseRepository.get_course_prerequisites(db, course)

        # Compose a plain dict payload (no ORM instances)
        info["attributes"] = attributes
        info["prerequisites"] = prerequisites or []
        return info

    @staticmethod
    async def prerequisites_met(
        db: AsyncSession,
        course: str,
        courses_taken: list[str],
    ) -> dict:
        """
        Checks if prerequisites for `course` are met given `courses_taken`.
        Returns: {"satisfied": bool, "message": str}
        """
        # Expect a list[list[str]] where each inner list is an OR-group
        prerequisite_groups = await CourseRepository.get_course_prerequisite_groups(db, course)
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

            # Your original logic: if any group is satisfied, the entire requirement is met
            # and missing should reset to empty.
            if group_satisfied:
                missing = []
                break
            else:
                missing.append(group_missing)

        if not missing:
            return {"satisfied": True, "message": "n/a"}

        # Build message like: "Take: CS2500 or CS5004;Take: MATH1341 or MATH1231;"
        parts: list[str] = []
        for group in missing:
            if not group:
                continue
            if len(group) == 1:
                parts.append(f"Take: {group[0]};")
            else:
                parts.append("Take: " + " or ".join(group) + ";")
        return {"satisfied": False, "message": "".join(parts)}

    @staticmethod
    async def get_select_courses(
        db: AsyncSession,
        courses: list[str],
    ) -> dict[str, dict | None]:
        """
        Fetch details for a list of courses. Sequential (no shared-session concurrency).
        Returns a mapping {course_code: course_data_or_None}
        """
        out: dict[str, dict | None] = {}
        for course in courses:
            out[course] = await CourseService.get_course_data(db, course)
        return out

    @staticmethod
    async def check_select_courses(
        db: AsyncSession,
        courses: list[str],
        courses_taken: list[str],
    ) -> dict[str, dict]:
        """
        Check prerequisites for a list of courses. Sequential (no shared-session concurrency).
        Returns a mapping {course_code: {"satisfied": bool, "message": str}}
        """
        out: dict[str, dict] = {}
        for course in courses:
            out[course] = await CourseService.prerequisites_met(db, course, courses_taken)
        return out

    @staticmethod
    async def search_courses(
        db: AsyncSession,
        query: str,
        limit: int,
    ) -> list[dict]:
        """
        Fuzzy-search course names/codes, returning a list of:
          { "course": <code>, "name": <name> }
        """
        # Expect repo to return a fully materialized list of dicts
        # with keys {"course": <code>, "name": <name>}
        rows = await CourseRepository.get_courses_like(db, query)
        items: dict[str, dict] = {}

        for row in rows:
            # Support both dict rows and tuple rows for safety
            if isinstance(row, dict):
                course_code = row.get("course")
                name = row.get("name")
            else:
                # Fallback tuple order: (course, name)
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
