from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Character
from .serializers import CharacterSerializer

class CharacterDetailView(generics.RetrieveAPIView):
    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return Character.objects.filter(user=self.request.user).first()

class CharacterCreateView(generics.CreateAPIView):
    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
