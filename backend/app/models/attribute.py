from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


# CREATE TABLE attributes (
#     attribute_id SERIAL PRIMARY KEY,
# tag TEXT,
# name TEXT
# );

class Attribute(Base):
    __tablename__ = "attributes"

    attribute_id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Attribute(attribute_id={self.attribute_id}, tag={self.tag}, name={self.name})"
