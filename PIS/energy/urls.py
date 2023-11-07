
from django.urls import path
from .views import home, registro, contactos, nosotros, paginaUsuario, inicioSesion, cerrarSesion

urlpatterns = [
    path('', home, name="home"),
    path('login/', inicioSesion, name="login"),
    path('registro/', registro, name="registro"),
    path('contactos/', contactos, name="contactos"),
    path('nosotros/', nosotros, name="nosotros"),
    path('paginaUsuario/', paginaUsuario, name="paginaUsuario"),
    path('cerrarSesion/', cerrarSesion, name="cerrarSesion"),
]