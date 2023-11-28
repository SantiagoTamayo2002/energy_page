from django.contrib import admin
from .models import Artefactos, Inventario, ConsumoDiarioMensual

# Register your models here.
admin.site.register(Artefactos)
admin.site.register(Inventario)
admin.site.register(ConsumoDiarioMensual)
