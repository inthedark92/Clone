from django.shortcuts import render, redirect
from django.contrib.auth import login
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

    context = {
        'player': user,
        'equipped_items': equipped_items,
        'next_level_exp': (user.level + 1) * 100
    }
    return render(request, 'game/character.html', context)

@login_required
def increase_stat(request):
    if request.method == 'POST':
        stat = request.POST.get('stat')
        user = request.user

        if user.stat_points <= 0:
            return JsonResponse({'error': 'Нет свободных очков характеристик.'}, status=400)

        if stat == 'intelligence' and user.level < 4:
            return JsonResponse({'error': 'Интеллект можно повышать только с 4 уровня.'}, status=400)

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
                'current_mp': user.current_mp
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
