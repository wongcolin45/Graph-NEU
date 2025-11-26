# app/root.py
from typing import List
from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.CourseFilter import CourseFilter
from app.dependencies import (
    get_course_service,
    get_graph_service,
    get_attribute_repository,
    get_department_repository
)
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.110.139.196:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

class CourseFilterRequest(BaseModel):
    departments: List[str]
    minCourseID: Optional[int] = None
    maxCourseID: Optional[int] = None
    attributes: List[str]

class CourseCheckRequest(BaseModel):
    coursesTaken: List[str]
    courses: List[str]


@app.post("/api/graph/course/{course}")
async def get_graph(
    course: str,
    req: Optional[CourseFilterRequest] = Body(...),
    graph_service = Depends(get_graph_service),
):
    departments = req.departments
    min_id = req.minCourseID
    max_id = req.maxCourseID
    attributes = req.attributes


    course_filter = CourseFilter(min_id, max_id, departments, attributes)

    try:
        # If GraphService is sync, you can await it if converted to async later
        return await graph_service.get_graph(course, course_filter)
    except Exception as e:
        return {"error": str(e), "message": "Something went wrong"}


@app.get("/api/course/{course}")
async def get_course(
    course: str,
    course_service = Depends(get_course_service)
):
    return await course_service.get_course(course)


@app.post("/api/course/check")
async def check_courses(
    body: CourseCheckRequest = Body(...),
    course_service = Depends(get_course_service)
):
    courses_taken = [c.replace(" ", "") for c in body.coursesTaken]
    courses = body.courses
    return await course_service.check_select_courses(courses, courses_taken)


@app.get("/api/course/search/{course}/{limit}")
async def search_courses(
    course: str,
    limit: int,
    course_service = Depends(get_course_service)
):
    if len(course) == 0:
        return []
    return await course_service.search_courses(course, limit)


@app.get("/api/departments/all")
async def get_all_departments(
    department_repository=Depends(get_department_repository)
):
    return await department_repository.get_departments()


@app.get("/api/attributes")
async def get_all_attributes(
    attribute_repository=Depends(get_attribute_repository)
):
    return await attribute_repository.get_all_attributes()
