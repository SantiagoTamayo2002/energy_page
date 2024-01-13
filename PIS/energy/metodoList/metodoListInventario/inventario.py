from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from energy.forms import InventarioForm
from energy.metodoList.metodoListInforme.informe import calcular_consumo_total_mensual
from energy.models import Inventario, Artefacto, Informe


def guardar_inventario_artefacto(request, form):
    inventario = form.save(commit=False)
    # Obtén el ID del artefacto desde el formulario
    artefacto = InventarioForm(request.user, request.POST).data['artefacto']
    # Verifica si ya existe un inventario para el usuario, el día y el artefacto
    if Inventario.objects.filter(user=request.user, dia=inventario.dia, artefacto_id=artefacto).exists():
        return messages.error(request, 'El artefacto ya existe en el inventario')
    else:
        inventario.user = request.user
        inventario.artefacto = Artefacto.objects.get(id=artefacto)
        inventario.consumo_artefacto = calcular_consumo_total(inventario.artefacto.consumo_wh,
                                                              inventario.artefacto.horas_de_uso,
                                                              inventario.cantidad_artefacto)
        inventario.save()
        Informe.actualizar_consumo_diario(request.user, inventario.dia, inventario.consumo_artefacto)
        return messages.success(request, 'El artefacto se agrego correctamente')

def eliminar_artefacto_inventario(request, inventario_id):
    try:
        inventario = Inventario.objects.get(pk=inventario_id)
    except Inventario.DoesNotExist:
        raise Http404("El Inventario no existe")
    # Guardar el día antes de eliminar el inventario
    dia_eliminado = inventario.dia
    inventario.delete()
    # Actualizar el consumo diario mensual para el día eliminado
    total = calcular_consumo_total_mensual(request.user)
    Informe.actualizar_consumo_diario(request.user, dia_eliminado, total)
    return redirect('inventario')


def eliminar_inventario(request):
    if request.user.is_anonymous:
        return redirect('home')
    inventario = Inventario.objects.filter(user=request.user)
    consumo = Informe.objects.filter(user=request.user)
    consumo.delete()
    inventario.delete()
    return redirect('inventario')


def calcular_consumo_total(consumo_wh, cantidadArtefacto, horasDeUso):
    consumo_total = (consumo_wh * cantidadArtefacto * horasDeUso).__round__(2)
    return consumo_total
