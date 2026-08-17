from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional, List
from app.schemas.player import Player, PlayerOut
from app.models.players import Players
import math
from app.services.scouting import get_features, euclidean_distance

router = APIRouter(
    prefix="/players",
    tags=['/Players']
)

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








@router.get("/{playername}/similarnopos")
def get_similar_players_noposition(playername: str, k: int = Query(default=10, ge=1, le=100), db:Session = Depends (get_db)):
    target_player = (
            db.query(Players).filter(Players.player_name == playername).first()
    )

    if target_player is None:
            raise HTTPException(
                status_code=404,
                detail="Player not found"
            )

    target_features = get_features(target_player)

    players = (
            db.query(Players)
            .filter(Players.player_name != playername)
            .all()
    )

    distances =[]


    for player in players:
            player_features = get_features(player)
    
            distance = euclidean_distance(
                target_features,
                player_features
            )
    
            distances.append((player, distance))
    
    distances.sort(key=lambda x: x[1])  
    nearest_players = distances[:k]
    return nearest_players







@router.get("/{playername}/similar")
def get_similar_players(playername: str, k: int = Query(default=10, ge=1, le=100), position: str = "", db:Session = Depends (get_db)):

    target_player = (
        db.query(Players).filter(Players.player_name == playername, Players.position == position).first()
    )

    if target_player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    target_features = get_features(target_player)

    players = (
        db.query(Players)
        .filter(Players.player_name != playername, Players.position == position)
        .all()
    )

    distances = []


    for player in players:
        player_features = get_features(player)

        distance = euclidean_distance(
            target_features,
            player_features
        )

        distances.append((player, distance))

    distances.sort(key=lambda x: x[1])
    nearest_players = distances[:k]
    return nearest_players




   





    

