from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Clan(Base):
    __tablename__ = "clans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    leader_id = Column(Integer, ForeignKey("characters.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), unique=True)
    balance = Column(Integer, default=0)

class MarketplaceItem(Base):
    __tablename__ = "marketplace_items"

    id = Column(Integer, primary_key=True, index=True)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    seller_id = Column(Integer, ForeignKey("characters.id"))
    price = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
