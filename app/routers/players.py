from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional, List
from app.schemas.player import Player, PlayerOut, similarPlayerOut
from app.models.players import Players
import math
from app.services.scouting import get_features, euclidean_distance

router = APIRouter(
    prefix="/players",
    tags=['/Players']
)




POSITION_WEIGHTS = {
    # Wingers
    # "RW":  [2.0, 1.2, 1.8, 1.6, 0.3, 0.7],
    "LW":  [2.0, 1.2, 1.8, 1.6, 0.3, 0.7],
    "RM":  [1.8, 1.0, 1.6, 1.7, 0.6, 0.8],
    "LM":  [1.8, 1.0, 1.6, 1.7, 0.6, 0.8],

    # Attackers
    "ST":  [1.3, 2.0, 1.2, 0.9, 0.2, 1.4],
    "CF":  [1.3, 1.8, 1.5, 1.4, 0.2, 1.1],

    # Attacking midfield
    "CAM": [1.0, 1.4, 1.8, 2.0, 0.4, 0.7],

    # Central midfield
    "CM":  [0.9, 0.9, 1.5, 2.0, 1.1, 1.1],
    "CDM": [0.8, 0.4, 1.0, 1.6, 2.0, 1.8],

    # Full backs
    "RB":  [1.5, 0.4, 1.0, 1.3, 1.8, 1.5],
    "LB":  [1.5, 0.4, 1.0, 1.3, 1.8, 1.5],

    # Wing backs
    "RWB": [1.8, 0.5, 1.3, 1.5, 1.5, 1.3],
    "LWB": [1.8, 0.5, 1.3, 1.5, 1.5, 1.3],

    # Centre backs
    "CB":  [0.6, 0.2, 0.5, 0.8, 2.0, 1.9],
}



@router.get("/", response_model=PlayerOut)
def get_players (db: Session = Depends(get_db), limit: int = 20, skip: int = 0, search: Optional[str] = ""):
    print (search)
    players =  db.query(Players).filter(Players.player_name.contains(search)).limit(limit).offset(skip).all()
    return players






@router.get("/{playername}", response_model=PlayerOut)
def get_one_player(playername: str, db: Session = Depends(get_db)):

    player_to_get = db.query(Players).filter(Players.player_name == playername).first()
    print (player_to_get)

    if not player_to_get:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = 
                            f"player with name: {playername} wasnt found")    
    return player_to_get



@router.get("/{playername}/similar", response_model=list[similarPlayerOut])
def get_similar_players(playername: str, k: int = Query(default=10, ge=1, le=100), position: str | None = None, league: str | None = None, db:Session = Depends (get_db)):


    
    target_player = (
        db.query(Players).filter(Players.player_name == playername).first()
    )

    if target_player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    target_features = get_features(target_player)

    weights = POSITION_WEIGHTS.get(
        target_player.position
    )



    players_query = (
        db.query(Players)
        .filter(Players.player_name != playername)
        
    )

    if position is not None:
        players_query = players_query.filter(
            Players.position == position
        )

    if league is not None:
        players_query = players_query.filter(
            Players.league == league
        )


    players = players_query.all()


    distances = []


    for player in players:
        player_features = get_features(player)

        distance = euclidean_distance(
            target_features,
            player_features,
            weights
        )

        distances.append((player, distance))

    distances.sort(key=lambda x: x[1])
    nearest_players = distances[:k]

    return [
        {
            "name": player.player_name,
            "position": player.position,
            "league": player.league,
            "similarity": round(distance, 2)
        }
        for player, distance in nearest_players
    ]



   





    

