from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


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
    dia = models.DateField(default=datetime.now)  # Usa datetime.now sin el .day
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