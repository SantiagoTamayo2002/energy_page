from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Artefactos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombreArtefacto = models.CharField(max_length=20)
    consumoKwH = models.FloatField(default=0)
    horasDeUso = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} Artefacto: {self.nombreArtefacto}"

class Inventario(models.Model):

    artefacto = models.ManyToManyField(Artefactos)
    dia = models.DateField(default=datetime.now().today())
    nombre = models.CharField(max_length=20)
    cantidadArtefactos = models.IntegerField()
    consumoTotalPorArtefacto = models.FloatField(default=0)
    consumoTotal = models.FloatField(default=0)
    def CalcularConsumoTotal(self):
        # Inicializar el consumo total
        consumoTotal = 0

        # Recorrer todos los artefactos en el inventario
        for artefacto in self.artefacto.all():
            consumoTotal += artefacto.consumoKwH * artefacto.horasDeUso
        return consumoTotal


    def save(self, *args, **kwargs):
        # Actualizar el valor de consumoTotal antes de guardar
        self.consumoTotal = self.CalcularConsumoTotal()
        super().save(*args, **kwargs)

    # Eliminar Artefacto
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Inventario para el artefacto: {self.nombre}'
