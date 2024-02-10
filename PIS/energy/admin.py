from django.contrib import admin
from .models import Artefacto, Inventario, Informe, UbicacionUsuario

# Register your models here.
admin.site.register(Artefacto)
admin.site.register(Inventario)
admin.site.register(Informe)
admin.site.register(UbicacionUsuario)

