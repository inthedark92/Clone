from sqlalchemy.orm import Session
from ..models.battle import Battle, BattleParticipant, BattleStatus, BattleType
from ..models.character import Character
from ..domain.battle.logic import BattleLogic
from .character_service import CharacterService
from typing import List, Dict

class BattleService:
    @staticmethod
    def start_pvp(p1: Character, p2: Character, db: Session) -> Battle:
        battle = Battle(battle_type=BattleType.PVP, status=BattleStatus.IN_PROGRESS)
        db.add(battle)
        db.flush() # Get ID

        # Snapshot stats
        p1_stats = CharacterService.calculate_stats(p1)
        p2_stats = CharacterService.calculate_stats(p2)

        part1 = BattleParticipant(
            battle_id=battle.id,
            character_id=p1.id,
            team=1,
            hp_snapshot=p1_stats['max_hp'],
            stats_snapshot=p1_stats
        )
        part2 = BattleParticipant(
            battle_id=battle.id,
            character_id=p2.id,
            team=2,
            hp_snapshot=p2_stats['max_hp'],
            stats_snapshot=p2_stats
        )

        db.add(part1)
        db.add(part2)
        db.commit()
        db.refresh(battle)
        return battle

    _pending_turns = {} # battle_id -> { char_id: action }

    @staticmethod
    def submit_turn(battle_id: int, char_id: int, action: Dict, db: Session):
        if battle_id not in BattleService._pending_turns:
            BattleService._pending_turns[battle_id] = {}

        BattleService._pending_turns[battle_id][char_id] = action

        battle = db.query(Battle).filter(Battle.id == battle_id).first()
        participants = db.query(BattleParticipant).filter(BattleParticipant.battle_id == battle_id).all()

        # Check if all participants submitted
        if len(BattleService._pending_turns[battle_id]) == len(participants):
            actions = BattleService._pending_turns.pop(battle_id)
            logic = BattleLogic(battle, participants)
            turn_logs = logic.process_turn(actions)

            # Append to log
            current_log = list(battle.log or [])
            current_log.append({"turn": battle.current_turn - 1, "events": turn_logs})
            battle.log = current_log

            db.commit()
            return battle, turn_logs

        return battle, None # Waiting for other player

    @staticmethod
    def get_battle_state(battle_id: int, db: Session):
        battle = db.query(Battle).filter(Battle.id == battle_id).first()
        participants = db.query(BattleParticipant).filter(BattleParticipant.battle_id == battle_id).all()
        return {
            "battle": battle,
            "participants": participants
        }
