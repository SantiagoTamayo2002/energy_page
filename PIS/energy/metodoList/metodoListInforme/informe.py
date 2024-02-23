from django.db.models import Sum
from energy.models import Informe
from datetime import datetime

# Función para calcular el consumo total mensual de un usuario
def calcular_consumo_total_mensual(usuario):
    # Obtener la suma del consumo total de todos los informes del usuario en el mes actual   
    consumo_mensual = Informe.objects.filter(user=usuario).aggregate(Sum('consumo_total'))[
                          'consumo_total__sum'] or 0
    # Convertir el consumo de Wh a kWh si el consumo mensual es diferente de cero    
    if consumo_mensual != 0:
        consumo_mensual = consumo_mensual / 1000
    # Retornar el consumo total mensual    
    return consumo_mensual

