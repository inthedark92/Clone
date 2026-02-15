from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import enum

class ItemType(enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    GLOVES = "gloves"
    BOOTS = "boots"
    SHIELD = "shield"
    RING = "ring"
    AMULET = "amulet"
    POTION = "potion"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    item_type = Column(SQLEnum(ItemType))

    # Requirements
    req_level = Column(Integer, default=1)
    req_strength = Column(Integer, default=0)
    req_agility = Column(Integer, default=0)
    req_intuition = Column(Integer, default=0)

    # Bonuses
    bonus_strength = Column(Integer, default=0)
    bonus_agility = Column(Integer, default=0)
    bonus_intuition = Column(Integer, default=0)
    bonus_endurance = Column(Integer, default=0)
    bonus_armor = Column(Integer, default=0)
    bonus_min_dmg = Column(Integer, default=0)
    bonus_max_dmg = Column(Integer, default=0)

    price = Column(Integer, default=0)

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    is_equipped = Column(Boolean, default=False)
    slot = Column(String, nullable=True) # e.g. "head", "main_hand", "off_hand"

    character = relationship("Character", back_populates="inventory")
    item = relationship("Item")
