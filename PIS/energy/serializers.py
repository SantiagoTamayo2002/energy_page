
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from energy.models import Artefacto, UbicacionUsuario

# Serializador para el modelo User
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # Los campos del modelo User que se incluirán en la representación serializada
        fields = ['first_name', 'last_name', 'email']

# Serializador para el modelo Artefacto
class ArtefactoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artefacto
        # Los campos del modelo Artefacto que se incluirán en la representación serializada
        fields = ['nombre_artefacto', 'consumo_wh', 'horas_de_uso']

# Serializador para el modelo UbicacionUsuario
class UbicacionUsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UbicacionUsuario
        # Los campos del modelo UbicacionUsuario que se incluirán en la representación serializada
        fields = ['latitud', 'longitud']
