from sqlalchemy.orm import Session

from app.repositories import CourseRepository
from rapidfuzz import process, fuzz

class CourseService:

    @staticmethod
    def get_course_data(db: Session, course):

        attributes = CourseRepository.get_course_attributes(db, course)
        info = CourseRepository.get_course_details(db, course)

        if info is None:
            return None

        info['attributes'] = attributes
        info['prerequisites'] = CourseRepository.get_course_prerequisites(db, course)
        return info

    @staticmethod
    def prerequisites_met(db: Session, course, courses_taken):
        prerequisites_groups = CourseRepository.get_course_prerequisite_groups(db, course)

        missing = []

        for group in prerequisites_groups:
            missing.append([])
            group_satisfied = False
            for course in group:
                if course in courses_taken:
                    group_satisfied = True
                else:
                    missing[-1].append(course)

            if group_satisfied:
                missing = []

        if len(missing) == 0:
            return {
                'satisfied': True,
                'message': 'n/a'
            }

        message = ''
        for group in missing:
            current = 'Take: '
            for i in range(0, len(group) - 1):
                current += group[i] + ' or '
            current += group[-1] + ';'
            message += current

        return {
            'satisfied': False,
            'message': message
        }

    @staticmethod
    def get_select_courses(db: Session, courses):
        courseData = {}
        for course in courses:
            data = CourseService.get_course_data(db, course)
            courseData[course] = data
        return courseData

    @staticmethod
    def check_select_courses(db: Session, courses, courses_taken):
        courses_status = {}

        for course in courses:

            courses_status[course] = CourseService.prerequisites_met(db, course, courses_taken)

        return courses_status

    @staticmethod
    def search_courses(db: Session, query: str, limit: int):
        results = CourseRepository.get_courses_like(db, query)

        items = {}
        for result in results:
            course_code = result[0]
            name = result[1]
            items[f'{course_code} {name}'] = {
                'course': course_code,
                'name': name,
            }

        matches = process.extract(
            query,
            items.keys(),
            scorer=fuzz.WRatio,
            limit=limit
        )

        clean = []
        for match in matches:
            matched_key = match[0]
            clean.append(items[matched_key])

        return clean
