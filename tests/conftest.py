import pytest

from app.database import SessionLocal
from app.models.players import Players


@pytest.fixture(scope="session", autouse=True)
def seed_test_database():
    db = SessionLocal()

    # Start clean
    db.query(Players).delete()

    players = [
        Players(
            player_name="Salah",
            player_age=34,
            pace=89,
            shooting=87,
            dribbling=88,
            passing=82,
            defending=45,
            physical=76,
            position="RW",
            league="Premier League"
        ),

        Players(
            player_name="Saka",
            player_age=24,
            pace=85,
            shooting=82,
            dribbling=87,
            passing=83,
            defending=60,
            physical=70,
            position="RW",
            league="Premier League"
        ),

        Players(
            player_name="Foden",
            player_age=26,
            pace=82,
            shooting=86,
            dribbling=90,
            passing=85,
            defending=57,
            physical=63,
            position="RW",
            league="Premier League"
        ),

        Players(
            player_name="Mbeumo",
            player_age=27,
            pace=88,
            shooting=82,
            dribbling=83,
            passing=76,
            defending=45,
            physical=75,
            position="RW",
            league="Premier League"
        ),

        Players(
            player_name="Rodrygo",
            player_age=25,
            pace=89,
            shooting=81,
            dribbling=88,
            passing=80,
            defending=31,
            physical=62,
            position="RW",
            league="La Liga"
        ),

        Players(
            player_name="Yamal",
            player_age=19,
            pace=85,
            shooting=81,
            dribbling=90,
            passing=86,
            defending=23,
            physical=53,
            position="RW",
            league="La Liga"
        ),

        Players(
            player_name="Raphinha",
            player_age=29,
            pace=91,
            shooting=84,
            dribbling=87,
            passing=82,
            defending=50,
            physical=72,
            position="RW",
            league="La Liga"
        ),
    ]

    db.add_all(players)
    db.commit()

    yield

    db.query(Players).delete()
    db.commit()
    db.close()