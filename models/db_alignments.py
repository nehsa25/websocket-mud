from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBAlignment(Base):
    __tablename__ = "alignments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]

    def __repr__(self) -> str:
        return f"DBAlignments(id={self.id!r}, name={self.name!r}, description={self.description!r})"