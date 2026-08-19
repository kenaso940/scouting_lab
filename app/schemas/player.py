from pydantic import BaseModel, ConfigDict

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
    position: str
    distance: float
    league: str


class PlayerOut(BaseModel):
    player_name: str
    player_age: int


class similarPlayerOut(BaseModel):
    name: str
    position: str
    league: str
    similarity: float
    model_config = ConfigDict(from_attributes=True)