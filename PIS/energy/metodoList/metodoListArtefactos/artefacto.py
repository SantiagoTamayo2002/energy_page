from django.contrib import messages
from django.shortcuts import redirect, render

from energy.models import Artefacto

def guardar_artefacto(request, form):
    artefacto = form.save(commit=False)
    # artefacto ya existe dentro del usuario
    if Artefacto.objects.filter(user=request.user, nombre_artefacto=artefacto.nombre_artefacto).exists():
        return messages.error(request, 'El artefacto ya existe')
    else:
        artefacto.user = request.user
        artefacto.save()
        return messages.success(request, 'El artefacto se agrego correctamente')






def eliminar_artefacto(request, artefacto_id):
    artefacto = Artefacto.objects.get(pk=artefacto_id)
    artefacto.delete()
    return redirect('artefacto')