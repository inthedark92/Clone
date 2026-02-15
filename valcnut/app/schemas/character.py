from pydantic import BaseModel
from typing import Optional, List

class CharacterBase(BaseModel):
    name: str

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(BaseModel):
    strength: Optional[int] = None
    agility: Optional[int] = None
    intuition: Optional[int] = None
    endurance: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    spirit: Optional[int] = None

class CharacterRead(CharacterBase):
    id: int
    level: int
    exp: int
    strength: int
    agility: int
    intuition: int
    endurance: int
    intelligence: int
    wisdom: int
    spirit: int
    stat_points: int
    current_hp: float
    current_mp: float
    location_id: str

    class Config:
        orm_mode = True
