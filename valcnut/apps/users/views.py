from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CharacterRegistrationForm

@login_required
def character_view(request):
    user = request.user
    # Get equipped items
    equipped_items = user.inventory.filter(is_equipped=True)

    stats_config = [
        ('strength', 'Сила', 0),
        ('agility', 'Ловкость', 0),
        ('intuition', 'Интуиция', 0),
        ('endurance', 'Выносливость', 0),
        ('intelligence', 'Интеллект', 4),
        ('wisdom', 'Мудрость', 7),
        ('spirit', 'Дух', 7),
    ]

    context = {
        'player': user,
        'equipped_items': equipped_items,
        'next_level_exp': user.next_level_exp,
        'stats_config': stats_config,
    }
    return render(request, 'game/character.html', context)

@login_required
def character_info_view(request, username=None, user_id=None):
    User = get_user_model()
    if user_id:
        player = get_object_or_404(User, id=user_id)
    else:
        player = get_object_or_404(User, username=username)

    equipped_items = player.inventory.filter(is_equipped=True)

    context = {
        'player': player,
        'equipped_items': equipped_items,
        'view_only': True
    }
    return render(request, 'game/character_info.html', context)

@login_required
def increase_stat(request):
    if request.method == 'POST':
        stat = request.POST.get('stat')
        user = request.user

        if user.stat_points <= 0:
            return JsonResponse({'error': 'Нет свободных очков характеристик.'}, status=400)

        if stat == 'intelligence' and user.level < 4:
            return JsonResponse({'error': 'Интеллект можно повышать только с 4 уровня.'}, status=400)

        if stat in ['wisdom', 'spirit'] and user.level < 7:
            return JsonResponse({'error': f'{stat.capitalize()} можно повышать только с 7 уровня.'}, status=400)

        valid_stats = ['strength', 'agility', 'intuition', 'endurance', 'intelligence', 'wisdom', 'spirit']
        if stat in valid_stats:
            current_val = getattr(user, stat)
            setattr(user, stat, current_val + 1)
            user.stat_points -= 1

            # Derived stats recovery/increase
            if stat == 'endurance':
                user.current_hp += 10
            elif stat == 'intelligence' and user.level >= 4:
                user.current_mp += 10

            user.save()
            return JsonResponse({
                'success': True,
                'stat': stat,
                'new_val': getattr(user, stat),
                'stat_points': user.stat_points,
                'max_hp': user.max_hp,
                'max_mp': user.max_mp,
                'current_hp': user.current_hp,
                'current_mp': user.current_mp,
                'damage': user.damage_range,
                'evasion': user.evasion,
                'crit': user.critical_chance,
                'defense': user.defense
            })

    return JsonResponse({'error': 'Некорректный запрос.'}, status=400)

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CharacterRegistrationForm
    success_url = reverse_lazy('game_index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
