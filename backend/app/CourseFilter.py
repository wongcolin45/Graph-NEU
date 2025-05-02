

class CourseFilter:

    def __init__(self, min_course_code = 0, max_course_code = 9000, department = None):
        self.min_course_code = min_course_code
        self.max_course_code = max_course_code
        self.department = department

    def get_min_course_code(self):
        return self.min_course_code

    def get_max_course_code(self):
        return self.max_course_code

    def get_department(self):
        return self.department

    def check(self, course_code, department):
        code_valid = self.min_course_code <= course_code <= self.max_course_code
        department_valid = self.department is None or department == self.department
        return code_valid and department_valid