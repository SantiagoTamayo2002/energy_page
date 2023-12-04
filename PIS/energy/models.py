from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Artefactos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombreArtefacto = models.CharField(max_length=20)
    consumoKwH = models.FloatField(default=0)
    horasDeUso = models.FloatField(default=0)
    inventario = models.ForeignKey('Inventario', related_name='artefsactoList', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.nombreArtefacto}"


class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dia = models.DateField(default=datetime.now)
    nombreArtefacto = models.CharField(max_length=30)
    horasDeUso = models.IntegerField(default=0)
    cantidadArtefactos = models.IntegerField()
    consumoArtefacto = models.FloatField(default=0)
    consumoTotal = models.FloatField(default=0)
    def __str__(self):
        return f'Inventario {self.user}: {self.nombreArtefacto}'


from django.db.models import Sum

class Informe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)
    dia = models.DateField(auto_now_add=True)  # Cambiado a auto_now_add para obtener la fecha actual en la creación del objeto
    consumoTotal = models.FloatField(default=0)  # Valor predeterminado actualizado a 0
    consumoTotalMensual = models.FloatField(default=0)

    @classmethod
    def actualizarConsumoDiario(cls, user, dia, total):
        # Obtener la suma total de consumoTotal para el usuario, inventario y día específicos
        mesActual = datetime.now().month
        consumo_total = Inventario.objects.filter(user=user, dia=dia, dia__month=mesActual).aggregate(Sum('consumoTotal'))['consumoTotal__sum'] or 0
        consumo_mensual = total
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