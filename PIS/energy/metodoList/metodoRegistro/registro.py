from django.contrib.auth import login
from django.contrib.auth.models import User

from energy.models import Perfil, UbicacionUsuario


def crear_usuario(request, latitud, longitud):
    # obtener ubicacion
    latitud = latitud
    longitud = longitud
    user = User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password1'], email=request.POST['email'],
                                    first_name=request.POST['first_name'],
                                    last_name=request.POST['last_name'])
    user_perfil = Perfil.objects.create(user=user)
    # Crear una instancia de Ubicacion Usuario y guardarla en la base de datos
    if latitud or longitud is not '':
        ubucacion_usuario = UbicacionUsuario.objects.create(
            user=user,
            latitud=latitud,
            longitud=longitud,
        )
        ubucacion_usuario.save()


    user.save()
    user_perfil.save()
    login(request, user)
