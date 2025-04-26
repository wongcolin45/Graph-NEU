from app.db.database import SessionLocal
from app.repositories.course_repo import CourseRepository
from app.services.graph_service import CourseGraphService

db = SessionLocal()

#result = CourseRepository.get_course_details(db, 'CS-3000')


#result = CourseRepository.get_course_prerequisites(db, "CS3000");

#result = CourseRepository.get_next_courses(db, 'CS2500')

result = CourseGraphService.get_graph(db, 'CS3000')


if result:

    # print(f"✅ Found course: {result.name} ({result.course_code})")
    print("RESULTS\n")
    print(result)
else:
    print("❌ No course found.")

db.close()
