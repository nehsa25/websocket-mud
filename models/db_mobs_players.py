from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class DBPlayer(Base):
    __tablename__ = "player_mobs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mobs.id"), unique=True, nullable=False)    
    mob = None

    def __repr__(self) -> str:
        return f"DBPlayer(id={self.id!r})"
