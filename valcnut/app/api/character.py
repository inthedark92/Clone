from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..api import deps
from ..models.user import User
from ..models.character import Character
from ..schemas.character import CharacterCreate, CharacterRead, CharacterUpdate
from ..services.character_service import CharacterService
from typing import List

router = APIRouter()

@router.post("/create", response_model=CharacterRead)
def create_character(
    char_in: CharacterCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # Check if user already has a character (limit to 1 for now)
    if current_user.characters:
        raise HTTPException(status_code=400, detail="Character already exists")

    character = Character(
        user_id=current_user.id,
        name=char_in.name,
        current_hp=60, # Initial HP
        current_mp=50  # Initial MP
    )
    db.add(character)
    db.commit()
    db.refresh(character)
    return character

@router.get("/me", response_model=CharacterRead)
def get_my_character(
    current_user: User = Depends(deps.get_current_active_user)
):
    if not current_user.characters:
        raise HTTPException(status_code=404, detail="Character not found")
    return current_user.characters[0]

@router.get("/{char_id}/stats")
def get_character_full_stats(
    char_id: int,
    db: Session = Depends(deps.get_db)
):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterService.calculate_stats(char)
