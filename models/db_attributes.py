from typing import Optional
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBAttributes(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    strength: Mapped[Optional[int]]
    agility: Mapped[Optional[int]]
    intelligence: Mapped[Optional[int]]
    wisdom: Mapped[Optional[int]]
    charisma: Mapped[Optional[int]]
    constitution: Mapped[Optional[int]]
    dexterity: Mapped[Optional[int]]
    luck: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"DBAttributes(id={self.id!r}, strength={self.strength!r}, agility={self.agility!r}, intelligence={self.intelligence!r}, wisdom={self.wisdom!r}, charisma={self.charisma!r}, constitution={self.constitution!r}, dexterity={self.dexterity!r}, luck={self.luck!r})"
    