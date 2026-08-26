

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Players(Base):
    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    player_name: Mapped[str] = mapped_column(
        String,
        primary_key=False,
        nullable=False
    )

    player_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    pace: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shooting: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dribbling: Mapped[int | None] = mapped_column(Integer, nullable=True)
    passing: Mapped[int | None] = mapped_column(Integer, nullable=True)
    defending: Mapped[int | None] = mapped_column(Integer, nullable=True)
    physical: Mapped[int | None] = mapped_column(Integer, nullable=True)

    position: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    league: Mapped[str] = mapped_column(
        String,
        nullable=False
    )


class PlayerStats(Base):
    __tablename__ = "player_stats"

    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.player_id"), nullable=False, primary_key=True)
    season: Mapped[int] = mapped_column(Integer, nullable=False)

    appearances: Mapped[int] = mapped_column(Integer, nullable=False)
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    goals: Mapped[int] = mapped_column(Integer, nullable=False)
    assists: Mapped[int] = mapped_column(Integer, nullable=False)

    shots_total: Mapped[int] = mapped_column(Integer, nullable=False)
    shots_on_target: Mapped[int] = mapped_column(Integer, nullable=False)

    passes_total: Mapped[int] = mapped_column(Integer, nullable=False)
    key_passes: Mapped[int] = mapped_column(Integer, nullable=False)

    pass_accuracy: Mapped[int] = mapped_column(Integer, nullable=False)
    tackles: Mapped[int] = mapped_column(Integer, nullable=False)

    interceptions: Mapped[int] = mapped_column(Integer, nullable=False)
    duels_total: Mapped[int] = mapped_column(Integer, nullable=False)

    duels_won: Mapped[int] = mapped_column(Integer, nullable=False)
    dribbles_attempted: Mapped[int] = mapped_column(Integer, nullable=False)

    dribbles_successful: Mapped[int] = mapped_column(Integer, nullable=False)
    fouls_drawn: Mapped[int] = mapped_column(Integer, nullable=False)

    fouls_committed: Mapped[int] = mapped_column(Integer, nullable=False)
    yellow_cards: Mapped[int] = mapped_column(Integer, nullable=False)
    red_cards: Mapped[int] = mapped_column(Integer, nullable=False)


        