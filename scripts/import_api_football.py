import time
import requests

from app.config import settings
from app.database import SessionLocal
from app.models.players import Players, PlayerStats


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

API_KEY = settings.api_football_key

if not API_KEY:
    raise RuntimeError("API_FOOTBALL_KEY is not set")


BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

LEAGUE_ID = 39
SEASON = 2024

# API-Football free plan page limit
MAX_PAGES = 3

# Stay below the free-plan request rate
REQUEST_DELAY = 7

# How many times to retry a request if API-Football
# responds with HTTP 429
MAX_RETRIES = 5

# Removes rows created by the old importer where
# every statistic was stored as 0
REMOVE_ZERO_MINUTE_PLAYERS = True


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def value_or_zero(value):
    """
    Convert API values to integers.

    API-Football sometimes returns None or numeric strings.
    """

    if value is None:
        return 0

    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def api_request(endpoint, params):
    """
    Make an API-Football request with rate limiting
    and automatic retry handling.
    """

    url = f"{BASE_URL}/{endpoint}"

    for attempt in range(1, MAX_RETRIES + 1):

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        # -------------------------------------------------
        # Rate limited
        # -------------------------------------------------

        if response.status_code == 429:
            wait_time = 60

            print(
                f"Rate limit reached. "
                f"Waiting {wait_time} seconds..."
            )

            time.sleep(wait_time)
            continue

        # -------------------------------------------------
        # Other HTTP errors
        # -------------------------------------------------

        response.raise_for_status()

        data = response.json()

        if data.get("errors"):
            raise RuntimeError(data["errors"])

        # Space requests out so we do not hit 429
        time.sleep(REQUEST_DELAY)

        return data

    raise RuntimeError(
        f"API request failed after {MAX_RETRIES} attempts"
    )


# ---------------------------------------------------------
# API requests
# ---------------------------------------------------------

def get_teams():
    """
    Retrieve all teams for the configured league and season.
    """

    data = api_request(
        "teams",
        {
            "league": LEAGUE_ID,
            "season": SEASON
        }
    )

    return data["response"]


def get_players(team_id, page):
    """
    Retrieve one page of players for a team.
    """

    return api_request(
        "players",
        {
            "team": team_id,
            "season": SEASON,
            "page": page
        }
    )


# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------

def remove_old_zero_stat_players(db):
    """
    Remove stale rows created by the original importer.

    The old importer converted completely empty API
    statistics into zeros and stored them in PostgreSQL.
    """

    zero_stats = (
        db.query(PlayerStats)
        .filter(PlayerStats.minutes == 0)
        .all()
    )

    if not zero_stats:
        print("No stale zero-minute players found.")
        return

    player_ids = [
        stats.player_id
        for stats in zero_stats
    ]

    print(
        f"Removing {len(player_ids)} stale "
        f"zero-minute player records..."
    )

    (
        db.query(PlayerStats)
        .filter(PlayerStats.player_id.in_(player_ids))
        .delete(synchronize_session=False)
    )

    (
        db.query(Players)
        .filter(Players.player_id.in_(player_ids))
        .delete(synchronize_session=False)
    )

    db.commit()


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

def save_player(db, api_player, stats):
    """
    Insert or update a player and their season statistics.
    """

    player_id = api_player["id"]

    # -----------------------------------------------------
    # Player
    # -----------------------------------------------------

    player = (
        db.query(Players)
        .filter(Players.player_id == player_id)
        .first()
    )

    if player is None:

        player = Players(
            player_id=player_id,
            player_name=api_player["name"],
            player_age=api_player["age"] or 0,

            # Temporary EA FC fields
            pace=None,
            shooting=None,
            dribbling=None,
            passing=None,
            defending=None,
            physical=None,

            position=(
                stats["games"]["position"]
                or "Unknown"
            ),

            league=stats["league"]["name"]
        )

        db.add(player)

    else:

        player.player_name = api_player["name"]
        player.player_age = api_player["age"] or 0

        player.position = (
            stats["games"]["position"]
            or "Unknown"
        )

        player.league = stats["league"]["name"]

    # Ensure player exists before FK insertion
    db.flush()

    # -----------------------------------------------------
    # Stats
    # -----------------------------------------------------

    stat_values = {

        "season": SEASON,

        "appearances": value_or_zero(
            stats["games"]["appearences"]
        ),

        "minutes": value_or_zero(
            stats["games"]["minutes"]
        ),

        "goals": value_or_zero(
            stats["goals"]["total"]
        ),

        "assists": value_or_zero(
            stats["goals"]["assists"]
        ),

        "shots_total": value_or_zero(
            stats["shots"]["total"]
        ),

        "shots_on_target": value_or_zero(
            stats["shots"]["on"]
        ),

        "passes_total": value_or_zero(
            stats["passes"]["total"]
        ),

        "key_passes": value_or_zero(
            stats["passes"]["key"]
        ),

        "pass_accuracy": value_or_zero(
            stats["passes"]["accuracy"]
        ),

        "tackles": value_or_zero(
            stats["tackles"]["total"]
        ),

        "interceptions": value_or_zero(
            stats["tackles"]["interceptions"]
        ),

        "duels_total": value_or_zero(
            stats["duels"]["total"]
        ),

        "duels_won": value_or_zero(
            stats["duels"]["won"]
        ),

        "dribbles_attempted": value_or_zero(
            stats["dribbles"]["attempts"]
        ),

        "dribbles_successful": value_or_zero(
            stats["dribbles"]["success"]
        ),

        "fouls_drawn": value_or_zero(
            stats["fouls"]["drawn"]
        ),

        "fouls_committed": value_or_zero(
            stats["fouls"]["committed"]
        ),

        "yellow_cards": value_or_zero(
            stats["cards"]["yellow"]
        ),

        "red_cards": value_or_zero(
            stats["cards"]["red"]
        )
    }

    player_stats = (
        db.query(PlayerStats)
        .filter(PlayerStats.player_id == player_id)
        .first()
    )

    if player_stats is None:

        player_stats = PlayerStats(
            player_id=player_id,
            **stat_values
        )

        db.add(player_stats)

    else:

        for field, value in stat_values.items():
            setattr(
                player_stats,
                field,
                value
            )


# ---------------------------------------------------------
# Import
# ---------------------------------------------------------

def import_players():

    db = SessionLocal()

    imported = 0
    skipped = 0

    try:

        # -------------------------------------------------
        # Remove bad rows from old importer
        # -------------------------------------------------

        if REMOVE_ZERO_MINUTE_PLAYERS:
            remove_old_zero_stat_players(db)

        # -------------------------------------------------
        # Teams
        # -------------------------------------------------

        teams = get_teams()

        print(
            f"\nFound {len(teams)} teams "
            f"for league {LEAGUE_ID}, "
            f"season {SEASON}"
        )

        # -------------------------------------------------
        # Process each team
        # -------------------------------------------------

        for team_item in teams:

            team = team_item["team"]

            team_id = team["id"]
            team_name = team["name"]

            print()
            print("=" * 60)
            print(f"Importing {team_name}")
            print("=" * 60)

            page = 1

            while page <= MAX_PAGES:

                print(
                    f"Fetching {team_name}, "
                    f"page {page}..."
                )

                data = get_players(
                    team_id=team_id,
                    page=page
                )

                # -----------------------------------------
                # Process players
                # -----------------------------------------

                for item in data["response"]:

                    api_player = item["player"]

                    # Find the correct league statistics
                    stats = next(
                        (
                            stat
                            for stat in item["statistics"]

                            if (
                                stat["league"]["id"]
                                == LEAGUE_ID

                                and
                                stat["league"]["season"]
                                == SEASON
                            )
                        ),
                        None
                    )

                    # No Premier League statistics
                    if stats is None:
                        skipped += 1
                        continue

                    minutes = value_or_zero(
                        stats["games"]["minutes"]
                    )

                    # -------------------------------------------------
                    # Important:
                    #
                    # Do not save players where API-Football
                    # returned no actual playing statistics.
                    # -------------------------------------------------

                    if minutes <= 0:
                        skipped += 1
                        continue

                    appearances = value_or_zero(
                        stats["games"]["appearences"]
                    )

                    print(
                        f'{api_player["id"]} | '
                        f'{api_player["name"]} | '
                        f'{appearances} apps | '
                        f'{minutes} mins'
                    )

                    save_player(
                        db,
                        api_player,
                        stats
                    )

                    imported += 1

                # Save after each page
                db.commit()

                # -----------------------------------------
                # Pagination
                # -----------------------------------------

                total_pages = data["paging"]["total"]

                if page >= total_pages:
                    break

                page += 1

        # -------------------------------------------------
        # Complete
        # -------------------------------------------------

        print()
        print("=" * 60)
        print("Import complete")
        print("=" * 60)

        print(
            f"Players imported/updated: {imported}"
        )

        print(
            f"Players skipped: {skipped}"
        )

        print(
            f"Players currently in database: "
            f"{db.query(Players).count()}"
        )

        print(
            f"Stats rows currently in database: "
            f"{db.query(PlayerStats).count()}"
        )

    except Exception as error:

        db.rollback()

        print()
        print("Import failed:")
        print(error)

        raise

    finally:
        db.close()


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    import_players()