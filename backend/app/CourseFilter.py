

class CourseFilter:

    def __init__(self,
                 min_course_code: int = 0,
                 max_course_code: int = 9000,
                 departments: list[str] = None,
                 attributes: list[str] = None):
        if departments is None:
            self.departments = []
        else:
            self.departments = departments

        if attributes is None:
            self.attributes = []
        else:
            self.attributes = attributes

        self.min_course_code = min_course_code
        self.max_course_code = max_course_code


    def get_min_course_code(self):
        return self.min_course_code

    def get_max_course_code(self):
        return self.max_course_code

    def has_departments(self):
        return len(self.departments) > 0

    def get_departments(self):
        return self.departments

    def has_attributes(self):
        return len(self.attributes) > 0

    def get_attributes(self):
        return self.attributes

    def check_attributes(self, course_attributes):
        if not self.has_attributes():
            return True
        for attribute in self.attributes:
            if attribute in course_attributes:
                return True
        return False

    def print(self):
        print(f'Filter ( Departments {self.departments}), min = {self.min_course_code}, max = {self.max_course_code}')



