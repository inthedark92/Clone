from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.item import Item, ItemType

class AdminService:
    @staticmethod
    def spawn_item(db: Session, item_data: dict) -> Item:
        item = Item(**item_data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def create_npc(db: Session, name: str, level: int):
        # NPCs can be stored in a separate table or as special characters
        pass
