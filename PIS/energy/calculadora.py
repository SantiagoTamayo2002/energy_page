from datetime import datetime
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import Artefactos, Inventario, ConsumoDiarioMensual

def calcularConsumoTotal(consumoTotalPorArtefacto, cantidadArtefactos, horasDeUso):
    consumoTotal = (consumoTotalPorArtefacto * cantidadArtefactos * horasDeUso).__round__(2)
    return consumoTotal

def calcularConsumoTotalMensual(user):
    mesActual = datetime.now().month
    consumo_mensual = ConsumoDiarioMensual.objects.filter(user=user, dia__month=mesActual).aggregate(Sum('consumoTotal'))['consumoTotal__sum'] or 0
    return consumo_mensual

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





