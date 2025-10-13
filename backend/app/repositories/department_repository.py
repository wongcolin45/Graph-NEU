from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Department


class DepartmentRepository:

    @staticmethod
    async def get_departments(db: AsyncSession):
        stmt = (
            select(
                Department.prefix.label("prefix"),
                Department.name.label("name"),
            )
            .select_from(Department)
            .order_by(Department.name.asc())
        )

        result = await db.execute(stmt)
        rows = result.all()
        return [dict(row._mapping) for row in rows]
