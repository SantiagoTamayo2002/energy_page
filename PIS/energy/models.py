from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Artefactos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombreArtefacto = models.CharField(max_length=20)
    consumoKwH = models.FloatField(default=0)
    horasDeUso = models.FloatField(default=0)
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombreArtefacto}"


class Inventario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artefacto = Artefactos.objects.all()
    dia = models.DateField(default=datetime.now)
    nombre = models.CharField(max_length=20)
    horasDeUso = models.IntegerField(default=0)
    cantidadArtefactos = models.IntegerField()
    consumoArtefacto = models.FloatField(default=0)
    consumoTotal = models.FloatField(default=0)

    def guardar(self, *args, **kwargs):
        # Actualizar el valor de consumoTotal antes de guardar
        self.consumoTotal = 0
        self.save()

    # Eliminar Artefacto
    def borrar(self, *args, **kwargs):
        self.delete()

    def __str__(self):
        return f'Inventario {self.user}: {self.nombre}'


from django.db.models import Sum

class ConsumoDiarioMensual(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.SET_NULL, null=True)
    dia = models.DateField(default=datetime.now)
    consumoTotal = models.FloatField(default=0)  # Valor predeterminado actualizado a 0

    @classmethod
    def actualizar_consumo_diario(cls, user, dia):
        # Obtener la suma total de consumoTotal para el usuario, inventario y día específicos
        consumo_total = Inventario.objects.filter(user=user, dia=dia).aggregate(Sum('consumoTotal'))['consumoTotal__sum'] or 0

        # Actualizar el campo consumoTotal con la suma
        cls.objects.update_or_create(
            user=user,
            dia=dia,
            defaults={'consumoTotal': consumo_total}
        )

    def __str__(self):
        return f'Consumo Diario {self.user}: {self.dia}'