from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Artefactos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombreArtefacto = models.CharField(max_length=20)
    consumoWH = models.FloatField(default=0)
    horasDeUso = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.nombreArtefacto}"


class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artefacto = models.ForeignKey(Artefactos, on_delete=models.SET_NULL, null=True, related_name="artefactoList")
    dia = models.DateField(default=datetime.now)
    cantidadArtefactos = models.PositiveIntegerField()
    consumoArtefacto = models.FloatField(default=0)
    def __str__(self):
        return f'Inventario {self.user}'


from django.db.models import Sum

class Informe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #relacion 1 a 1 con inventario
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True, related_name="inventario")
    dia = models.DateField(auto_now_add=True)  # Cambiado a auto_now_add para obtener la fecha actual en la creación del objeto
    consumoTotal = models.FloatField(default=0)  # Valor predeterminado actualizado a 0
    consumoTotalMensual = models.FloatField(default=0)

    @classmethod
    def actualizarConsumoDiario(cls, user, dia, consumoTotalMensual):
        # Obtener la suma total de consumoTotal para el usuario, inventario y día específicos
        mesActual = datetime.now().month
        consumo_total = Inventario.objects.filter(user=user, dia=dia, dia__month=mesActual).aggregate(Sum('consumoArtefacto'))['consumoArtefacto__sum'] or 0
        consumo_mensual = consumoTotalMensual
        # Actualizar el campo consumoTotal con la suma
        cls.objects.update_or_create(
            user=user,
            dia=dia,
            defaults={
                'consumoTotal': consumo_total.__round__(2),
                'consumoTotalMensual': consumo_mensual.__round__(2)
            }
        )


    def __str__(self):
        return f'Consumo Diario {self.user}: {self.dia}'