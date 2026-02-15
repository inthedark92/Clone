from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CharacterRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            "username": "Имя персонажа",
            "email": "Email (необязательно)",
        }
