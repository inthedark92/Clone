from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum as SQLEnum, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class BattleStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"

class BattleType(enum.Enum):
    PVP = "pvp"
    PVE = "pve"

class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(SQLEnum(BattleStatus), default=BattleStatus.PENDING)
    battle_type = Column(SQLEnum(BattleType))
    current_turn = Column(Integer, default=1)

    # Stores the full history of moves
    log = Column(JSON, default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

class BattleParticipant(Base):
    __tablename__ = "battle_participants"

    id = Column(Integer, primary_key=True, index=True)
    battle_id = Column(Integer, ForeignKey("battles.id"))
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    npc_id = Column(String, nullable=True) # For PvE
    team = Column(Integer) # 1 or 2

    # Snapshot of stats at the beginning of the battle
    hp_snapshot = Column(Integer)
    stats_snapshot = Column(JSON)

    is_winner = Column(Boolean, default=False)
