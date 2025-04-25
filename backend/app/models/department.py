from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Department(Base):
    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Department(id={self.department_id}, prefix={self.prefix}, name={self.name})"
