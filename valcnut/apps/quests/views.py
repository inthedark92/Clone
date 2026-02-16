from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Quest, PlayerQuest

@login_required
def quest_list(request):
    quests = Quest.objects.all()
    player_quests = PlayerQuest.objects.filter(user=request.user)
    return render(request, 'quests/list.html', {'quests': quests, 'player_quests': player_quests})
