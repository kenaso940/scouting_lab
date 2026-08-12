from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PlayerBase (BaseModel):
    player_name: str
    player_age: int

class Player(PlayerBase):
    pace: int
    shooting: int
    dribbling: int
    passing: int
    physical: int
    defending: int
