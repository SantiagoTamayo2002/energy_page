from datetime import datetime
from django.db.models import Sum
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import numpy as np
from .models import Artefactos, Inventario, ConsumoDiarioMensual


def calcularConsumoTotal(consumoTotalPorArtefacto, cantidadArtefactos, horasDeUso):
    consumoTotal = (consumoTotalPorArtefacto * cantidadArtefactos * horasDeUso).__round__(2)
    return consumoTotal

def calcularConsumoTotalMensual(user):
    mesActual = datetime.now().month
    consumoMensual = ConsumoDiarioMensual.objects.filter(user=user, dia__month=mesActual).aggregate(Sum('consumoTotal'))['consumoTotal__sum'] or 0
    return consumoMensual

def eliminarArtefacto(request, artefacto_id):
    artefacto = Artefactos.objects.get(pk=artefacto_id)
    artefacto.delete()
    return redirect('artefacto')



def eliminarDiaEnInventario(request, inventario_id):
    try:
        inventario = Inventario.objects.get(pk=inventario_id)
    except Inventario.DoesNotExist:
        raise Http404("El Inventario no existe")
    # Guardar el día antes de eliminar el inventario
    dia_eliminado = inventario.dia
    inventario.delete()
    # Actualizar el consumo diario mensual para el día eliminado
    total = calcularConsumoTotalMensual(request.user)
    ConsumoDiarioMensual.actualizarConsumoDiario(request.user, dia_eliminado, total)
    return redirect('inventario')




# def generarGrafico(request):
#     # Generar datos aleatorios
#     try:
#         mesActual = datetime.now().month
#         consumoMensual = ConsumoDiarioMensual.objects.filter(user=request.user, dia__month=mesActual)
#         x = []
#         y = []
#         numro = 0
#         for consumo in consumoMensual:
#             print(consumo.dia, consumo.consumoTotal)
#             x.append(numro)
#             y.append(consumo.consumoTotal)
#             print(x)
#             print(y)
#             numro += 1
#
#         x = np.array(x)
#         y = np.array(y)
#         data = {
#             'x': x.tolist(),
#             'y': y.tolist(),
#         }
#         return JsonResponse(data)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)



