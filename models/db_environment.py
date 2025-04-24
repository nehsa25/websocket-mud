from sqlalchemy import Column, Integer, String
from models.base import Base


class DBEnvironment(Base):
    __tablename__ = "environment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    def __repr__(self):
        return f"<DBEnvironment(name='{self.name}')>"
