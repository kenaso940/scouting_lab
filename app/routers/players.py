from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Depends
from sqlalchemy.orm import Session
from .. database import get_db
from typing import Optional, List
from app.schemas.player import Player
from app.models.players import Players

router = APIRouter(
    prefix="/players",
    tags=['/Players']
)

@router.get("/", response_model=Player)
def get_players (db: Session = Depends(get_db), limit: int = 20, skip: int = 0, search: Optional[str] = ""):

    print (search)

    players =  db.query(Players).filter(Players.player_name.contains(search)).limit(limit).offset(skip).all()
    return players


@router.get("/{playername}", response_model=Player)
def get_one_player(playername: str, db: Session = Depends(get_db)):

    player_to_get = db.query(Players).filter(Players.player_name == playername).first()
    print (player_to_get)

    if not player_to_get:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = 
                            f"player with name: {playername} wasnt found")    
    return player_to_get

    