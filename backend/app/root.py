from typing import List

from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.dependencies import get_db
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

@app.get('/api/graph/course/{course}')
async def get_graph(course, db: Session = Depends(get_db)):
    try:
        return GraphService.get_graph(db, course)
    except Exception as e:
        return {"error": str(e), "message": "Something went wrong"}

@app.get('/api/course/{course}')
async def get_course(course, db: Session = Depends(get_db)):
    return CourseService.get_course_data(db, course)

@app.get('/api/course/select')
async def get_select_courses(courses, db: Session = Depends(get_db)):
    #return CourseService.get_select_courses(db: Session, courses)
    return {'endpoint not implemented'}


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

