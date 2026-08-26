import pytest

from app.database import SessionLocal
from app.models.players import Players, PlayerStats


@pytest.fixture(scope="session")
def seed_test_database():
    db = SessionLocal()

    try:
        # -------------------------------------------------
        # Start clean
        #
        # PlayerStats must be deleted first because it has
        # a foreign key referencing Players.
        # -------------------------------------------------

        db.query(PlayerStats).delete()
        db.query(Players).delete()
        db.commit()

        # -------------------------------------------------
        # Players
        # -------------------------------------------------

        players = [
            Players(
                player_id=1,
                player_name="Salah",
                player_age=34,
                position="RW",
                league="Premier League"
            ),

            Players(
                player_id=2,
                player_name="Saka",
                player_age=24,
                position="RW",
                league="Premier League"
            ),

            Players(
                player_id=3,
                player_name="Foden",
                player_age=26,
                position="RW",
                league="Premier League"
            ),

            Players(
                player_id=4,
                player_name="Mbeumo",
                player_age=27,
                position="RW",
                league="Premier League"
            ),

            Players(
                player_id=5,
                player_name="Rodrygo",
                player_age=25,
                position="RW",
                league="La Liga"
            ),

            Players(
                player_id=6,
                player_name="Yamal",
                player_age=19,
                position="RW",
                league="La Liga"
            ),

            Players(
                player_id=7,
                player_name="Raphinha",
                player_age=29,
                position="RW",
                league="La Liga"
            ),
        ]

        db.add_all(players)
        db.flush()

        # -------------------------------------------------
        # Player statistics
        # -------------------------------------------------

        stats = [
            PlayerStats(
                player_id=1,
                season=2024,
                appearances=38,
                minutes=3370,
                goals=29,
                assists=18,
                shots_total=130,
                shots_on_target=70,
                passes_total=1450,
                key_passes=90,
                pass_accuracy=82,
                tackles=18,
                interceptions=7,
                duels_total=310,
                duels_won=150,
                dribbles_attempted=120,
                dribbles_successful=65,
                fouls_drawn=55,
                fouls_committed=20,
                yellow_cards=3,
                red_cards=0
            ),

            PlayerStats(
                player_id=2,
                season=2024,
                appearances=30,
                minutes=2500,
                goals=12,
                assists=10,
                shots_total=85,
                shots_on_target=42,
                passes_total=1200,
                key_passes=70,
                pass_accuracy=84,
                tackles=35,
                interceptions=12,
                duels_total=280,
                duels_won=145,
                dribbles_attempted=115,
                dribbles_successful=62,
                fouls_drawn=60,
                fouls_committed=25,
                yellow_cards=4,
                red_cards=0
            ),

            PlayerStats(
                player_id=3,
                season=2024,
                appearances=28,
                minutes=2200,
                goals=10,
                assists=8,
                shots_total=75,
                shots_on_target=38,
                passes_total=1350,
                key_passes=75,
                pass_accuracy=88,
                tackles=25,
                interceptions=10,
                duels_total=220,
                duels_won=110,
                dribbles_attempted=100,
                dribbles_successful=60,
                fouls_drawn=45,
                fouls_committed=20,
                yellow_cards=2,
                red_cards=0
            ),

            PlayerStats(
                player_id=4,
                season=2024,
                appearances=36,
                minutes=3000,
                goals=20,
                assists=8,
                shots_total=110,
                shots_on_target=55,
                passes_total=1000,
                key_passes=55,
                pass_accuracy=78,
                tackles=28,
                interceptions=9,
                duels_total=350,
                duels_won=180,
                dribbles_attempted=125,
                dribbles_successful=60,
                fouls_drawn=50,
                fouls_committed=35,
                yellow_cards=5,
                red_cards=0
            ),

            PlayerStats(
                player_id=5,
                season=2024,
                appearances=32,
                minutes=2700,
                goals=14,
                assists=9,
                shots_total=95,
                shots_on_target=48,
                passes_total=1300,
                key_passes=72,
                pass_accuracy=86,
                tackles=20,
                interceptions=8,
                duels_total=260,
                duels_won=125,
                dribbles_attempted=140,
                dribbles_successful=78,
                fouls_drawn=52,
                fouls_committed=22,
                yellow_cards=3,
                red_cards=0
            ),

            PlayerStats(
                player_id=6,
                season=2024,
                appearances=35,
                minutes=2900,
                goals=9,
                assists=15,
                shots_total=90,
                shots_on_target=43,
                passes_total=1550,
                key_passes=105,
                pass_accuracy=87,
                tackles=22,
                interceptions=9,
                duels_total=300,
                duels_won=155,
                dribbles_attempted=190,
                dribbles_successful=115,
                fouls_drawn=75,
                fouls_committed=20,
                yellow_cards=2,
                red_cards=0
            ),

            PlayerStats(
                player_id=7,
                season=2024,
                appearances=34,
                minutes=2800,
                goals=18,
                assists=12,
                shots_total=115,
                shots_on_target=58,
                passes_total=1400,
                key_passes=85,
                pass_accuracy=83,
                tackles=30,
                interceptions=11,
                duels_total=330,
                duels_won=165,
                dribbles_attempted=150,
                dribbles_successful=82,
                fouls_drawn=65,
                fouls_committed=30,
                yellow_cards=6,
                red_cards=0
            ),
        ]

        db.add_all(stats)
        db.commit()

        yield

    finally:
        # -------------------------------------------------
        # Clean up test data
        # -------------------------------------------------

        db.rollback()

        db.query(PlayerStats).delete()
        db.query(Players).delete()

        db.commit()
        db.close()