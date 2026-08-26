from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.player import PlayerOut, similarPlayerOut
from app.models.players import Players, PlayerStats

from app.services.scouting import (
    get_features,
    normalize_feature_vectors,
    euclidean_distance,
    MIN_MINUTES,
)


router = APIRouter(
    prefix="/players",
    tags=["Players"]
)


# ---------------------------------------------------------
# Feature order
# ---------------------------------------------------------
#
# 0   goals / 90
# 1   assists / 90
# 2   shots / 90
# 3   shot-on-target rate
#
# 4   passes / 90
# 5   key passes / 90
# 6   pass accuracy
#
# 7   tackles / 90
# 8   interceptions / 90
#
# 9   duels / 90
# 10  duel win rate
#
# 11  dribble attempts / 90
# 12  dribble success rate
#
# 13  fouls drawn / 90
# 14  fouls committed / 90
# ---------------------------------------------------------


POSITION_WEIGHTS = {

    # -----------------------------------------------------
    # Detailed positions
    # Useful if we later improve position classification
    # -----------------------------------------------------

    "RW": [
        1.6, 1.4, 1.6, 1.3,
        0.8, 1.4, 0.8,
        0.5, 0.4,
        0.9, 0.8,
        1.8, 1.6,
        1.2, 0.5
    ],

    "LW": [
        1.6, 1.4, 1.6, 1.3,
        0.8, 1.4, 0.8,
        0.5, 0.4,
        0.9, 0.8,
        1.8, 1.6,
        1.2, 0.5
    ],

    "RM": [
        1.1, 1.3, 1.2, 1.1,
        1.1, 1.5, 1.0,
        0.8, 0.7,
        1.0, 0.9,
        1.5, 1.4,
        1.1, 0.7
    ],

    "LM": [
        1.1, 1.3, 1.2, 1.1,
        1.1, 1.5, 1.0,
        0.8, 0.7,
        1.0, 0.9,
        1.5, 1.4,
        1.1, 0.7
    ],

    "ST": [
        2.0, 1.1, 1.8, 1.6,
        0.5, 0.8, 0.6,
        0.3, 0.2,
        1.2, 1.1,
        0.9, 0.8,
        1.0, 0.6
    ],

    "CF": [
        1.7, 1.4, 1.5, 1.4,
        0.8, 1.2, 0.8,
        0.4, 0.3,
        1.1, 1.0,
        1.1, 1.0,
        1.1, 0.6
    ],

    "CAM": [
        1.2, 1.6, 1.2, 1.1,
        1.2, 2.0, 1.2,
        0.5, 0.5,
        0.9, 0.8,
        1.5, 1.3,
        1.3, 0.6
    ],

    "CM": [
        0.8, 1.1, 0.8, 0.8,
        1.7, 1.5, 1.5,
        1.2, 1.2,
        1.2, 1.1,
        1.0, 1.0,
        1.0, 0.9
    ],

    "CDM": [
        0.4, 0.6, 0.5, 0.5,
        1.6, 1.1, 1.4,
        1.8, 2.0,
        1.6, 1.6,
        0.6, 0.7,
        0.7, 1.0
    ],

    "RB": [
        0.5, 0.8, 0.7, 0.7,
        1.2, 1.1, 1.1,
        1.7, 1.5,
        1.5, 1.4,
        1.2, 1.1,
        0.9, 1.0
    ],

    "LB": [
        0.5, 0.8, 0.7, 0.7,
        1.2, 1.1, 1.1,
        1.7, 1.5,
        1.5, 1.4,
        1.2, 1.1,
        0.9, 1.0
    ],

    "RWB": [
        0.7, 1.0, 0.9, 0.8,
        1.3, 1.3, 1.1,
        1.4, 1.2,
        1.4, 1.3,
        1.5, 1.3,
        1.1, 0.9
    ],

    "LWB": [
        0.7, 1.0, 0.9, 0.8,
        1.3, 1.3, 1.1,
        1.4, 1.2,
        1.4, 1.3,
        1.5, 1.3,
        1.1, 0.9
    ],

    "CB": [
        0.2, 0.3, 0.3, 0.4,
        1.2, 0.5, 1.4,
        1.8, 2.0,
        1.8, 1.8,
        0.3, 0.5,
        0.5, 1.0
    ],


    # -----------------------------------------------------
    # API-Football broad positions
    #
    # These are the important ones right now because
    # API-Football currently gives us broad positions.
    # -----------------------------------------------------

    "Attacker": [
        1.8, 1.3, 1.6, 1.4,
        0.6, 1.0, 0.7,
        0.3, 0.3,
        1.1, 1.0,
        1.2, 1.1,
        1.1, 0.6
    ],

    "Forward": [
        1.8, 1.3, 1.6, 1.4,
        0.6, 1.0, 0.7,
        0.3, 0.3,
        1.1, 1.0,
        1.2, 1.1,
        1.1, 0.6
    ],

    "Midfielder": [
        0.8, 1.2, 0.8, 0.8,
        1.6, 1.6, 1.4,
        1.2, 1.3,
        1.2, 1.1,
        1.0, 1.0,
        1.0, 0.8
    ],

    "Defender": [
        0.3, 0.4, 0.4, 0.5,
        1.2, 0.7, 1.3,
        1.8, 1.9,
        1.7, 1.7,
        0.6, 0.7,
        0.6, 1.0
    ],
}


# ---------------------------------------------------------
# Get players
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[PlayerOut]
)
def get_players(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = ""
):

    players = (
        db.query(Players)
        .filter(
            Players.player_name.contains(search)
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    return players


# ---------------------------------------------------------
# Get one player
# ---------------------------------------------------------

@router.get(
    "/{playername}",
    response_model=PlayerOut
)
def get_one_player(
    playername: str,
    db: Session = Depends(get_db)
):

    player = (
        db.query(Players)
        .filter(
            Players.player_name == playername
        )
        .first()
    )

    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Player with name "
                f"'{playername}' was not found"
            )
        )

    return player


# ---------------------------------------------------------
# Find similar players
# ---------------------------------------------------------

@router.get(
    "/{playername}/similar",
    response_model=list[similarPlayerOut]
)
def get_similar_players(
    playername: str,
    k: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    position: str | None = None,
    league: str | None = None,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Find target player
    # -----------------------------------------------------

    target_player = (
        db.query(Players)
        .filter(
            Players.player_name == playername
        )
        .first()
    )

    if target_player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )


    # -----------------------------------------------------
    # Find target player's statistics
    # -----------------------------------------------------

    target_stats = (
        db.query(PlayerStats)
        .filter(
            PlayerStats.player_id
            == target_player.player_id
        )
        .first()
    )

    if target_stats is None:
        raise HTTPException(
            status_code=400,
            detail="Player has no statistics"
        )


    # -----------------------------------------------------
    # Minimum playing time
    # -----------------------------------------------------

    if target_stats.minutes < MIN_MINUTES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Player has only "
                f"{target_stats.minutes} minutes. "
                f"Minimum required is "
                f"{MIN_MINUTES} minutes."
            )
        )


    # -----------------------------------------------------
    # Goalkeepers require a different feature set
    # -----------------------------------------------------

    if target_player.position == "Goalkeeper":
        raise HTTPException(
            status_code=400,
            detail=(
                "Goalkeeper similarity is not "
                "currently supported"
            )
        )


    # -----------------------------------------------------
    # Candidate player query
    # -----------------------------------------------------

    players_query = (
        db.query(
            Players,
            PlayerStats
        )
        .join(
            PlayerStats,
            Players.player_id
            == PlayerStats.player_id
        )
        .filter(
            Players.player_id
            != target_player.player_id
        )
        .filter(
            PlayerStats.minutes
            >= MIN_MINUTES
        )
        .filter(
            Players.position
            != "Goalkeeper"
        )
    )


    # -----------------------------------------------------
    # Optional position filter
    # -----------------------------------------------------

    if position is not None:

        position = position.strip()

        players_query = (
            players_query.filter(
                Players.position == position
            )
        )


    # -----------------------------------------------------
    # Optional league filter
    # -----------------------------------------------------

    if league is not None:

        league = league.strip()

        players_query = (
            players_query.filter(
                Players.league == league
            )
        )


    players = players_query.all()

    if not players:
        return []


    # -----------------------------------------------------
    # Create raw target feature vector
    # -----------------------------------------------------

    target_features = get_features(
        target_stats
    )


    # -----------------------------------------------------
    # Create candidate feature vectors
    # -----------------------------------------------------

    candidate_features = [
        get_features(stats)
        for _, stats in players
    ]


    # -----------------------------------------------------
    # Normalize features
    #
    # Important because something like passes/90 could
    # otherwise dominate something like goals/90 simply
    # because it has much larger numbers.
    # -----------------------------------------------------

    all_features = [
        target_features,
        *candidate_features
    ]

    normalized_features = (
        normalize_feature_vectors(
            all_features
        )
    )

    normalized_target = (
        normalized_features[0]
    )

    normalized_candidates = (
        normalized_features[1:]
    )


    # -----------------------------------------------------
    # Get weights based on target player's position
    # -----------------------------------------------------

    weights = POSITION_WEIGHTS.get(
        target_player.position
    )


    # -----------------------------------------------------
    # Calculate player distances
    # -----------------------------------------------------

    distances = []

    for (
        (player, stats),
        player_features
    ) in zip(
        players,
        normalized_candidates
    ):

        distance = euclidean_distance(
            normalized_target,
            player_features,
            weights
        )

        distances.append(
            (
                player,
                distance
            )
        )


    # -----------------------------------------------------
    # Sort closest first
    # -----------------------------------------------------

    distances.sort(
        key=lambda result: result[1]
    )


    # -----------------------------------------------------
    # Keep nearest K players
    # -----------------------------------------------------

    nearest_players = distances[:k]
 

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return [
        {
            "name": player.player_name,
            "position": player.position,
            "league": player.league,

            # This is currently technically a distance:
            # lower = more similar.
            "similarity": round(
                distance,
                2
            )
        }

        for player, distance
        in nearest_players
    ]