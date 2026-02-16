from rest_framework import serializers
from .models import Battle, BattleParticipant, Monster

class MonsterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monster
        fields = '__all__'

class BattleParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleParticipant
        fields = '__all__'

class BattleSerializer(serializers.ModelSerializer):
    participants = BattleParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Battle
        fields = '__all__'
