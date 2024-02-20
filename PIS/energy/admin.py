from django.contrib import admin
from .models import Artefacto, Inventario, Informe, UbicacionUsuario, ModoClaro, Perfil

# Register your models here.
admin.site.register(Artefacto)
admin.site.register(Inventario)
admin.site.register(Informe)
admin.site.register(UbicacionUsuario)
admin.site.register(ModoClaro)
admin.site.register(Perfil)

