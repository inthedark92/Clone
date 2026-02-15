from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..api import deps
from ..models.user import User
from ..models.character import Character
from ..services.battle_service import BattleService
from ..domain.battle.engine import HitZone
from typing import List, Dict

router = APIRouter()

@router.post("/challenge/{target_id}")
def challenge_player(
    target_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    p1 = current_user.characters[0]
    p2 = db.query(Character).filter(Character.id == target_id).first()

    if not p2:
        raise HTTPException(status_code=404, detail="Target player not found")

    battle = BattleService.start_pvp(p1, p2, db)
    return {"battle_id": battle.id, "status": battle.status}

@router.post("/{battle_id}/turn")
def submit_turn(
    battle_id: int,
    attack_zone: int,
    block_zones: List[int],
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    p1 = current_user.characters[0]

    action = {
        "attack": HitZone(attack_zone),
        "blocks": [HitZone(z) for z in block_zones]
    }

    battle, logs = BattleService.submit_turn(battle_id, p1.id, action, db)

    if logs is None:
        return {"status": "waiting_for_opponent"}

    return {"battle": battle, "turn_logs": logs}
