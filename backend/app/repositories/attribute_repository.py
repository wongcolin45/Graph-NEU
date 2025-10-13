from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Attribute


class AttributeRepository:

    @staticmethod
    async def get_all_attributes(db: AsyncSession):
        stmt = (
            select(
                Attribute.tag.label("tag"),
                Attribute.name.label("name"),
            )
            .select_from(Attribute)
            .order_by(Attribute.name.asc())
        )

        result = await db.execute(stmt)
        rows = result.all()  # list[Row]
        # Row -> dict via _mapping (stable API)
        return [dict(row._mapping) for row in rows]
