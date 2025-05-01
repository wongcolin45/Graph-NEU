from typing import List

from fastapi import FastAPI, Body

from app.db.database import SessionLocal
from app.repositories.course_repo import CourseRepository
from app.services.course_service import CourseService
from app.services.graph_service import GraphService

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SessionLocal()

# PYTHONPATH=backend uvicorn app.root:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/api/graph/course/{course}')
async def get_graph(course):
    try:
        return GraphService.get_graph(db, course)
    except Exception as e:
        return {"error": str(e), "message": "Something went wrong"}

@app.get('/api/course/{course}')
async def get_course(course):
    return CourseRepository.get_course_data(db, course)

@app.get('/api/course/select')
async def get_select_courses(courses):
    return CourseService.get_select_courses(db, courses)



class CourseCheckRequest(BaseModel):
    coursesTaken: List[str]
    courses: List[str]

@app.post('/api/course/check')
def check_courses(req: CourseCheckRequest = Body(...)):
    courses_taken = req.coursesTaken
    courses = req.courses

    for i in range(len(courses_taken)):
        courses_taken[i] = courses_taken[i].replace(' ','')

    result = CourseService.check_select_courses(db, courses, courses_taken)


    return result


@app.get('/api/majors')
def get_majors():
    return ['Computer Science', 'Data Science']