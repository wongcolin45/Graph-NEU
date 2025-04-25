from app.db.database import SessionLocal
from app.repositories.course_repo import CourseRepository

db = SessionLocal()

#result = CourseRepository.get_course_details(db, 'CS-3000')

#result = CourseRepository.get_course_attributes(db, "CS", 3000)
#result = CourseRepository.get_course_prerequisites(db, "CS", "3000");
#result = CourseRepository.get_course_data(db, 'CS-3000')
result = CourseRepository.get_next_courses(db, 'CS2500')
#result = CourseRepository.get_course_data(db, 'CS3000')
if result:
    # print(f"✅ Found course: {result.name} ({result.course_code})")
    print("RESULTS\n")
    print(result)
else:
    print("❌ No course found.")

db.close()
