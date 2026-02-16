from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'level', 'exp', 'gold', 'silver', 'diamonds',
            'strength', 'agility', 'intuition', 'endurance', 'intelligence', 'wisdom', 'spirit',
            'stat_points', 'current_hp', 'current_mp', 'last_location', 'clan', 'alliance'
        ]
