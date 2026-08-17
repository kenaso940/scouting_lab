from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.database import Base


class Players(Base):
    __tablename__ = "players"

    player_name = Column(String, primary_key=True, nullable = False)
    player_age = Column(Integer, nullable=False)
    pace = Column(Integer, nullable=False)
    shooting = Column(Integer, nullable=False)
    dribbling = Column(Integer, nullable=False)
    passing = Column(Integer, nullable=False)
    defending = Column(Integer, nullable=False)
    physical = Column(Integer, nullable=False)
    position = Column(String, nullable=False)



