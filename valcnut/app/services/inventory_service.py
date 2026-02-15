from sqlalchemy.orm import Session
from ..models.item import Item, InventoryItem, ItemType
from ..models.character import Character
from fastapi import HTTPException

class InventoryService:
    @staticmethod
    def equip_item(character: Character, inventory_item_id: int, db: Session):
        inv_item = db.query(InventoryItem).filter(
            InventoryItem.id == inventory_item_id,
            InventoryItem.character_id == character.id
        ).first()

        if not inv_item:
            raise HTTPException(status_code=404, detail="Item not found in inventory")

        item = inv_item.item

        # Check requirements
        if character.level < item.req_level:
            raise HTTPException(status_code=400, detail="Level too low")

        # Determine slot
        slot = None
        if item.item_type == ItemType.HELMET: slot = "head"
        elif item.item_type == ItemType.ARMOR: slot = "body"
        elif item.item_type == ItemType.WEAPON: slot = "main_hand"
        elif item.item_type == ItemType.SHIELD: slot = "off_hand"
        # ... more slots ...

        # Unequip current item in that slot
        current_in_slot = db.query(InventoryItem).filter(
            InventoryItem.character_id == character.id,
            InventoryItem.slot == slot,
            InventoryItem.is_equipped == True
        ).first()
        if current_in_slot:
            current_in_slot.is_equipped = False
            current_in_slot.slot = None

        inv_item.is_equipped = True
        inv_item.slot = slot
        db.commit()
        return inv_item

    @staticmethod
    def buy_item(character: Character, item_id: int, db: Session):
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # In a real game, check gold. Here we just add it.
        new_inv_item = InventoryItem(character_id=character.id, item_id=item_id)
        db.add(new_inv_item)
        db.commit()
        db.refresh(new_inv_item)
        return new_inv_item
