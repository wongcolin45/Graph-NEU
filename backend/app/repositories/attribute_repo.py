



from sqlalchemy import String, cast
from sqlalchemy.orm import Session, aliased
from app.models import Attribute


class AttributeRepository:

    @staticmethod
    def get_all_attributes(db: Session):
        results = (
            db.query(
                Attribute.tag.label('tag'),
                Attribute.name.label('name')
            ).select_from(Attribute)
            .all()
        )
        return [row._asdict() for row in results]
