from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class DBDirection(Base):
    __tablename__ = "directions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    variations = Column(String)
    opposite_id = Column(Integer, ForeignKey("directions.id"), nullable=True)  # Foreign key to self
    opposite = relationship(
        "DBDirection",
        remote_side=[id],
        foreign_keys=[opposite_id],
        uselist=False,
    )

    def __repr__(self):
        return f"<DBDirection(name='{self.name}')>"
