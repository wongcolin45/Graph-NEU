
from typing import List

from fastapi import FastAPI, Body, Depends, Query
from sqlalchemy.orm import Session

from app.CourseFilter import CourseFilter
from app.db.database import SessionLocal
from app.dependencies import get_db
from app.repositories.attribute_repo import AttributeRepository
from app.repositories.department_repo import DepartmentRepository
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



# PYTHONPATH=backend uvicorn app.root:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}


class CourseFilterRequest(BaseModel):
    departments: List[str]
    minCourseID: int
    maxCourseID: int
    attributes: List[str]

@app.post('/api/graph/course/{course}')
async def get_graph(course, req: CourseFilterRequest = Body(...), db: Session = Depends(get_db)):
    departments = req.departments
    min = req.minCourseID
    max = req.maxCourseID
    attributes = req.attributes

    print("\n\n\nCHECKINGG GRAPH REQUEST ")
    print(departments)
    print(min)
    print(max)
    print(attributes)
    print('=====================\n\n\n')

    filter = CourseFilter(min, max, departments, attributes)

    try:
        return GraphService.get_graph(db, course, filter)
    except Exception as e:
        return {"error": str(e), "message": "Something went wrong"}

# ==============================================================
# GET Graph Endpoint
# ==============================================================
@app.get('/api/course/{course}')
async def get_course(course: str, db: Session = Depends(get_db)):
    return CourseService.get_course_data(db, course)


class CourseCheckRequest(BaseModel):
    coursesTaken: List[str]
    courses: List[str]

@app.post('/api/course/check')
def check_courses(req: CourseCheckRequest = Body(...), db: Session = Depends(get_db)):
    courses_taken = req.coursesTaken
    courses = req.courses

    for i in range(len(courses_taken)):
        courses_taken[i] = courses_taken[i].replace(' ','')

    result = CourseService.check_select_courses(db, courses, courses_taken)


    return result



@app.get('/api/course/search/{course}/{limit}')
def search_courses(course: str, limit: int, db: Session = Depends(get_db)):

    if len(course) == 0:
        return []

    results = CourseService.search_courses(db, course, limit)

    return results


@app.get('/api/departments/all')
def get_all_departments(db: Session = Depends(get_db)):
    return DepartmentRepository.get_departments(db)


@app.get('/api/attributes')
def get_all_attributes(db: Session = Depends(get_db)):
    return AttributeRepository.get_all_attributes(db)