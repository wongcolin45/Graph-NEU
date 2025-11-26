# app/dependencies.py
from typing import AsyncGenerator
from fastapi import Depends
from app.db.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import CourseRepository, DepartmentRepository
from app.repositories.attribute_repository import AttributeRepository
from app.services import GraphService
from app.services.course_service import CourseService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_course_service(db: AsyncSession = Depends(get_db)) -> CourseService:
    repository = CourseRepository(db)
    return CourseService(repository)

async def get_graph_service(course_service = Depends(get_course_service)) -> GraphService:
    return GraphService(course_service)


async def get_attribute_repository(db: AsyncSession = Depends(get_db)) -> AttributeRepository:
    return AttributeRepository(db)

async def get_department_repository(db: AsyncSession = Depends(get_db)) -> DepartmentRepository:
    return DepartmentRepository(db)