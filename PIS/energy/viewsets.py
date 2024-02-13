from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Artefacto, UbicacionUsuario
from .serializers import UserSerializer, ArtefactoSerializer, UbicacionUsuarioSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArtefactoViewSet(viewsets.ModelViewSet):
    queryset = Artefacto.objects.all()
    serializer_class = ArtefactoSerializer

class UbicacionUsuarioViewSet(viewsets.ModelViewSet):
    queryset = UbicacionUsuario.objects.all()
    serializer_class = UbicacionUsuarioSerializer
