# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql.expression import text
# from sqlalchemy.orm import relationship
# from app.database import Base


# class Players(Base):
#     __tablename__ = "players"

#     player_name = Column(String, primary_key=True, nullable = False)
#     player_age = Column(Integer, nullable=False)
#     pace = Column(Integer, nullable=False)
#     shooting = Column(Integer, nullable=False)
#     dribbling = Column(Integer, nullable=False)
#     passing = Column(Integer, nullable=False)
#     defending = Column(Integer, nullable=False)
#     physical = Column(Integer, nullable=False)
#     position = Column(String, nullable=False)
#     league = Column(String, nullable=False)



from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Players(Base):
    __tablename__ = "players"

    player_name: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        nullable=False
    )

    player_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    pace: Mapped[int] = mapped_column(Integer, nullable=False)
    shooting: Mapped[int] = mapped_column(Integer, nullable=False)
    dribbling: Mapped[int] = mapped_column(Integer, nullable=False)
    passing: Mapped[int] = mapped_column(Integer, nullable=False)
    defending: Mapped[int] = mapped_column(Integer, nullable=False)
    physical: Mapped[int] = mapped_column(Integer, nullable=False)

    position: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    league: Mapped[str] = mapped_column(
        String,
        nullable=False
    )