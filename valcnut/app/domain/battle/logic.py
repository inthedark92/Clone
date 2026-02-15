from typing import List, Dict, Optional
from .engine import BattleEngine, HitZone, BattleResultType
from ...models.battle import Battle, BattleParticipant

class BattleLogic:
    def __init__(self, battle_model: Battle, participants: List[BattleParticipant]):
        self.battle = battle_model
        self.participants = {p.character_id: p for p in participants if p.character_id}
        # For NPCs
        self.npc_participants = {p.npc_id: p for p in participants if p.npc_id}

    def process_turn(self, actions: Dict[int, Dict]) -> List[Dict]:
        """
        actions: { character_id: { "attack": HitZone, "blocks": [HitZone, HitZone] } }
        """
        turn_logs = []

        # In a 1v1 PvP
        ids = list(self.participants.keys())
        if len(ids) != 2:
            return [{"error": "Only 1v1 supported currently"}]

        p1_id, p2_id = ids[0], ids[1]
        p1_actions = actions.get(p1_id)
        p2_actions = actions.get(p2_id)

        if not p1_actions or not p2_actions:
            return [{"error": "Actions missing for one or more players"}]

        # Resolve P1 attacking P2
        logs_1to2 = self.resolve_attack(p1_id, p2_id, p1_actions, p2_actions)
        turn_logs.extend(logs_1to2)

        # Resolve P2 attacking P1
        logs_2to1 = self.resolve_attack(p2_id, p1_id, p2_actions, p1_actions)
        turn_logs.extend(logs_2to1)

        self.battle.current_turn += 1
        return turn_logs

    def resolve_attack(self, attacker_id, defender_id, attacker_actions, defender_actions) -> List[Dict]:
        attacker = self.participants[attacker_id]
        defender = self.participants[defender_id]

        logs = []

        # Main Hand Attack
        res = BattleEngine.calculate_damage(
            attacker.stats_snapshot,
            defender.stats_snapshot,
            attacker_actions['attack'],
            defender_actions['blocks']
        )

        self.apply_damage(defender, res['damage'])
        logs.append({
            "attacker_id": attacker_id,
            "defender_id": defender_id,
            "type": res['type'].name,
            "damage": res['damage'],
            "hit_zone": res.get('hit_zone'),
            "defender_hp_left": defender.hp_snapshot
        })

        # Off-hand Attack if dual wielding
        if attacker.stats_snapshot.get('is_dual_wielding'):
            res_off = BattleEngine.calculate_damage(
                attacker.stats_snapshot,
                defender.stats_snapshot,
                attacker_actions['attack'], # Same zone or random? Usually same in these games
                defender_actions['blocks'],
                is_offhand=True
            )
            self.apply_damage(defender, res_off['damage'])
            logs.append({
                "attacker_id": attacker_id,
                "defender_id": defender_id,
                "type": res_off['type'].name,
                "damage": res_off['damage'],
                "is_offhand": True,
                "defender_hp_left": defender.hp_snapshot
            })

        return logs

    def apply_damage(self, participant: BattleParticipant, damage: int):
        participant.hp_snapshot = max(0, participant.hp_snapshot - damage)
        if participant.hp_snapshot <= 0:
            from ...models.battle import BattleStatus
            self.battle.status = BattleStatus.FINISHED
            # Determine winner
            for p_id, p in self.participants.items():
                if p.hp_snapshot > 0:
                    p.is_winner = True
                else:
                    p.is_winner = False
