# app/repositories/attribute_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AttributeORM


class AttributeRepository:
    """Interface for interacting with attributes in database"""

    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_attributes(self):
        query = (
            select(
                AttributeORM.tag.label("tag"),
                AttributeORM.name.label("name"),
            )
            .select_from(AttributeORM)
            .order_by(AttributeORM.name.asc())
        )
        result = await self.db.execute(query)
        rows = result.all()  # list[Row]
        return [dict(row._mapping) for row in rows]
