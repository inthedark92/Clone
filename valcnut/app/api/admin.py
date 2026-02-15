from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..api import deps
from ..models.user import User, UserRole
from ..models.character import Character
from ..models.item import Item, ItemType
from ..schemas.character import CharacterUpdate
from ..services.admin_service import AdminService

router = APIRouter()

def check_admin(current_user: User = Depends(deps.get_current_active_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.put("/character/{char_id}/stats", dependencies=[Depends(check_admin)])
def admin_edit_stats(
    char_id: int,
    stats: CharacterUpdate,
    db: Session = Depends(deps.get_db)
):
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    for key, value in stats.dict(exclude_unset=True).items():
        setattr(char, key, value)

    db.commit()
    return {"message": "Stats updated successfully"}

@router.post("/item/spawn", dependencies=[Depends(check_admin)])
def spawn_item(
    name: str,
    item_type: str,
    db: Session = Depends(deps.get_db)
):
    item_data = {
        "name": name,
        "item_type": ItemType[item_type.upper()],
        "price": 100
    }
    item = AdminService.spawn_item(db, item_data)
    return item

@router.post("/user/{user_id}/ban", dependencies=[Depends(check_admin)])
def ban_user(
    user_id: int,
    db: Session = Depends(deps.get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"message": f"User {user.username} has been banned"}
