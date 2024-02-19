from django.contrib import messages
from django.shortcuts import redirect

from energy.forms import ActualizarUsuarioForm, ActualizarPerfilForm


def actualizar_perfil_usuario(request, form, perfil_form):

    if form.is_valid() and perfil_form.is_valid():
        if request.user.perfil.imagen:
            request.user.perfil.imagen.delete()
        form.save()
        perfil_form.save()
        return messages.success(request, 'Perfil actualizado correctamente')
    else:
        messages.error(request, 'Error al actualizar el perfil')