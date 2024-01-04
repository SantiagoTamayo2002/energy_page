from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect


class Artefacto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_artefacto = models.CharField(max_length=20)
    consumo_wh = models.FloatField(default=0)
    horas_de_uso = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.nombre_artefacto}"


class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artefacto = models.ForeignKey(Artefacto, on_delete=models.SET_NULL, null=True, related_name="artefacto_list")
    dia = models.DateField(default=datetime.now)
    cantidad_artefacto = models.PositiveIntegerField()
    consumo_artefacto = models.FloatField(default=0)
    def __str__(self):
        return f'Inventario {self.user}'


from django.db.models import Sum

class Informe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #relacion 1 a 1 con inventario
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True, related_name="inventario_list")
    dia = models.DateField(auto_now_add=True)  # Cambiado a auto_now_add para obtener la fecha actual en la creación del objeto
    consumo_total = models.FloatField(default=0)  # Valor predeterminado actualizado a 0
    consumo_total_mensual = models.FloatField(default=0)

    @classmethod
    def actualizar_consumo_diario(cls, user, dia, consumo_total_mensual):
        # Obtener la suma total de consumoArticulo para el usuario, inventario y día específicos
        consumo_total = Inventario.objects.filter(user=user, dia=dia).aggregate(Sum('consumo_artefacto'))['consumo_artefacto__sum']

        # Verificar si consumo_total es None y asignar 0 si es el caso
        consumo_total = consumo_total if consumo_total is not None else 0

        consumo_mensual = consumo_total_mensual

        # Actualizar el campo consumoTotal con la suma
        cls.objects.update_or_create(
            user=user,
            dia=dia,
            defaults={
                'consumo_total': round(consumo_total, 2),
                'consumo_total_mensual': round(consumo_mensual, 2)
            }
        )

    def __str__(self):
        return f'Consumo Diario {self.user}: {self.dia}'