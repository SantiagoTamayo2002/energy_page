from django.db.models import Sum
from energy.models import Informe
from datetime import datetime


def calcular_consumo_total_mensual(usuario):
    consumo_mensual = Informe.objects.filter(user=usuario).aggregate(Sum('consumo_total'))[
                          'consumo_total__sum'] or 0
    if consumo_mensual != 0:
        consumo_mensual = consumo_mensual / 1000
    return consumo_mensual

