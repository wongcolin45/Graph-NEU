from fastapi import FastAPI

from app.db.database import SessionLocal
from app.repositories.course_repo import CourseRepository
from app.services.graph_service import GraphService
app = FastAPI()
db = SessionLocal()

# PYTHONPATH=backend uvicorn app.root:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/api/graph/course/{course}')
async def get_graph(course):
    return GraphService.get_graph(db, course)


@app.get('/api/course/{course}')
async def get_course(course):
    return CourseRepository.get_course_data(db, course)