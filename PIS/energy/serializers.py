
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from energy.models import Artefacto


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ArtefactoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artefacto
        fields = ['nombre_artefacto', 'consumo_wh', 'horas_de_uso']
