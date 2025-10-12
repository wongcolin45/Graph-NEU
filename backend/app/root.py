from typing import List
from fastapi import FastAPI, Body, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.CourseFilter import CourseFilter
from app.dependencies import get_db
from app.repositories.attribute_repo import AttributeRepository
from app.repositories.department_repo import DepartmentRepository
from app.services.course_service import CourseService
from app.services.graph_service import GraphService


app = FastAPI()

# --------------------------
# CORS middleware
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
"http://10.110.139.196:3000",   # add this
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Root test endpoint
# --------------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}


# --------------------------
# Request models
# --------------------------
class CourseFilterRequest(BaseModel):
    departments: List[str]
    minCourseID: int
    maxCourseID: int
    attributes: List[str]


class CourseCheckRequest(BaseModel):
    coursesTaken: List[str]
    courses: List[str]


# ==============================================================
# GRAPH ENDPOINTS
# ==============================================================
@app.post("/api/graph/course/{course}")
async def get_graph(
    course: str,
    req: CourseFilterRequest = Body(...),
    db: AsyncSession = Depends(get_db),
):
    departments = req.departments
    min_id = req.minCourseID
    max_id = req.maxCourseID
    attributes = req.attributes

    # print("\n\n\nCHECKING GRAPH REQUEST")
    # print(departments)
    # print(min_id)
    # print(max_id)
    # print(attributes)
    # print("=====================\n\n\n")

    course_filter = CourseFilter(min_id, max_id, departments, attributes)

    try:
        # If GraphService is sync, you can await it if converted to async later
        return await GraphService.get_graph(db, course, course_filter)
    except Exception as e:
        return {"error": str(e), "message": "Something went wrong"}


# ==============================================================
# COURSE ENDPOINTS
# ==============================================================
@app.get("/api/course/{course}")
async def get_course(course: str, db: AsyncSession = Depends(get_db)):
    return await CourseService.get_course_data(db, course)


@app.post("/api/course/check")
async def check_courses(req: CourseCheckRequest = Body(...), db: AsyncSession = Depends(get_db)):
    courses_taken = [c.replace(" ", "") for c in req.coursesTaken]
    courses = req.courses
    return await CourseService.check_select_courses(db, courses, courses_taken)


@app.get("/api/course/search/{course}/{limit}")
async def search_courses(course: str, limit: int, db: AsyncSession = Depends(get_db)):
    if len(course) == 0:
        return []
    return await CourseService.search_courses(db, course, limit)


# ==============================================================
# DEPARTMENTS & ATTRIBUTES
# ==============================================================
@app.get("/api/departments/all")
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    return await DepartmentRepository.get_departments(db)


@app.get("/api/attributes")
async def get_all_attributes(db: AsyncSession = Depends(get_db)):
    return await AttributeRepository.get_all_attributes(db)
