from .engine import BattleEngine

class BattleLogic:
    def __init__(self, battle, participants):
        self.battle = battle
        self.participants = {p.user_id: p for p in participants if p.user_id}

    def process_turn(self, actions):
        turn_logs = []
        ids = list(self.participants.keys())
        if len(ids) != 2:
            return [{"error": "Only 1v1 supported"}]

        p1_id, p2_id = ids[0], ids[1]
        p1_actions = actions.get(p1_id)
        p2_actions = actions.get(p2_id)

        if not p1_actions or not p2_actions:
            return [{"error": "Missing actions"}]

        turn_logs.extend(self.resolve_attack(p1_id, p2_id, p1_actions, p2_actions))
        turn_logs.extend(self.resolve_attack(p2_id, p1_id, p2_actions, p1_actions))

        self.battle.current_turn += 1
        return turn_logs

    def resolve_attack(self, attacker_id, defender_id, attacker_actions, defender_actions):
        attacker = self.participants[attacker_id]
        defender = self.participants[defender_id]
        logs = []

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
            "type": res['type'].name if hasattr(res['type'], 'name') else str(res['type']),
            "damage": res['damage'],
            "hit_zone": int(res.get('hit_zone', 0)),
            "defender_hp_left": defender.hp_snapshot
        })

        if attacker.stats_snapshot.get('is_dual_wielding'):
            res_off = BattleEngine.calculate_damage(
                attacker.stats_snapshot,
                defender.stats_snapshot,
                attacker_actions['attack'],
                defender_actions['blocks'],
                is_offhand=True
            )
            self.apply_damage(defender, res_off['damage'])
            logs.append({
                "attacker_id": attacker_id,
                "defender_id": defender_id,
                "type": res_off['type'].name if hasattr(res_off['type'], 'name') else str(res_off['type']),
                "damage": res_off['damage'],
                "is_offhand": True,
                "defender_hp_left": defender.hp_snapshot
            })
        return logs

    def apply_damage(self, participant, damage):
        participant.hp_snapshot = max(0, participant.hp_snapshot - damage)
        if participant.hp_snapshot <= 0:
            self.battle.status = 'finished'
            self.battle.save()
            self.finalize_battle()
        participant.save()

    def finalize_battle(self):
        import random
        from django.db.models import F

        all_participants = self.battle.participants.all()
        winners = [p for p in all_participants if p.hp_snapshot > 0]

        for p in all_participants:
            if p.hp_snapshot > 0:
                p.is_winner = True
            else:
                p.is_winner = False
            p.save()

            if p.user:
                # Decrease durability of equipped items
                p.user.inventory.filter(is_equipped=True).update(
                    durability_current=F('durability_current') - 1
                )

                if p.is_winner and self.battle.battle_type == 'pve':
                    # Find monster
                    monster_p = all_participants.exclude(npc_id__isnull=True).first()
                    if monster_p:
                        stats = monster_p.stats_snapshot
                        gold_gain = random.randint(stats.get('gold_min', 0), stats.get('gold_max', 0) + 1)
                        p.user.gold += gold_gain
                        p.user.add_exp(stats.get('exp', 0))
                        p.user.save()
