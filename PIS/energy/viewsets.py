from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Artefacto
from .serializers import UserSerializer, ArtefactoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArtefactoViewSet(viewsets.ModelViewSet):
    queryset = Artefacto.objects.all()
    serializer_class = ArtefactoSerializer
