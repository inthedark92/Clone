from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CharacterRegistrationForm

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CharacterRegistrationForm
    success_url = reverse_lazy('game_index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
