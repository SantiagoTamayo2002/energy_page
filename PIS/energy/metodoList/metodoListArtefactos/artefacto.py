from django.contrib import messages
from django.shortcuts import redirect, render
# Importar el modelo Artefacto desde energy.models
from energy.models import Artefacto

# Función para guardar un nuevo artefacto en la base de datos
def guardar_artefacto(request, form):
    # Guardar el artefacto del formulario en la variable artefacto
    artefacto = form.save(commit=False)
    # Verificar si el artefacto ya existe para el usuario actual
    if Artefacto.objects.filter(user=request.user, nombre_artefacto=artefacto.nombre_artefacto).exists():
        # Mostrar un mensaje de error si el artefacto ya existe        
        return messages.error(request, 'El artefacto ya existe')
    else:
        # Asignar el usuario actual al artefacto y guardarlo en la base de datos
        artefacto.user = request.user
        artefacto.save()
        # Mostrar un mensaje de éxito indicando que el artefacto se agregó correctamente        
        return messages.success(request, 'El artefacto se agrego correctamente')





# Función para eliminar un artefacto de la base de datos
def eliminar_artefacto(request, artefacto_id):
    # Obtener el objeto Artefacto correspondiente al artefacto_id especificado
    artefacto = Artefacto.objects.get(pk=artefacto_id)
    # Eliminar el artefacto de la base de datos    
    artefacto.delete()
    # Redirigir al usuario a la página de artefactos después de eliminar exitosamente el artefacto
    return redirect('artefacto')