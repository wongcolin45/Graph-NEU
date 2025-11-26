# app/repositories/department_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import DepartmentORM


class DepartmentRepository:
    """Interface for interacting with departments in database"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_departments(self):
        query = (
            select(
                DepartmentORM.prefix.label("prefix"),
                DepartmentORM.name.label("name"),
            )
            .select_from(DepartmentORM)
            .order_by(DepartmentORM.name.asc())
        )
        result = await self.db.execute(query)
        rows = result.all()
        return [dict(row._mapping) for row in rows]
