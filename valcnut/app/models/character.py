from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum as SQLEnum, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class CharacterClass(enum.Enum):
    WARRIOR = "warrior"
    ROGUE = "rogue"
    MAGE = "mage"

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, unique=True, index=True)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)

    # Base Stats
    strength = Column(Integer, default=3)
    agility = Column(Integer, default=3)
    intuition = Column(Integer, default=3)
    endurance = Column(Integer, default=3)
    intelligence = Column(Integer, default=3)
    wisdom = Column(Integer, default=3)
    spirit = Column(Integer, default=3)

    # Free stat points
    stat_points = Column(Integer, default=0)

    # Current State
    current_hp = Column(Float)
    current_mp = Column(Float)

    # Location
    location_id = Column(String, default="central_square")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="characters")
    inventory = relationship("InventoryItem", back_populates="character")

    @property
    def max_hp(self):
        return 30 + (self.endurance * 10)

    @property
    def max_mp(self):
        return 20 + (self.wisdom * 10)
