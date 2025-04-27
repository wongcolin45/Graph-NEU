from sqlalchemy.orm import Session

from app.repositories import CourseRepository


class CourseService:

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
