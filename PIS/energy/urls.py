
from django.urls import path
from .views import home, registro, contactos, nosotros, paginaUsuario, inicioSesion, cerrarSesion, inventario, artefacto, eliminarArtefacto

urlpatterns = [
    path('', home, name="home"),
    path('login/', inicioSesion, name="login"),
    path('registro/', registro, name="registro"),
    path('contactos/', contactos, name="contactos"),
    path('nosotros/', nosotros, name="nosotros"),
    path('paginaUsuario/', paginaUsuario, name="paginaUsuario"),
    path('c', cerrarSesion, name="cerrarSesion"),
    path('paginaUsuario/inventario/', inventario, name="inventario"),
   # path('paginaUsuario/inventario/<int:artefacto_id>/', agregarArtefactoInventario, name='agregarArtefactoInventario'),
    path('paginaUsuario/inventario/artefactos/', artefacto, name="artefacto"),
    path('paginaUsuario/inventario/artefactos/<int:artefacto_id>/', eliminarArtefacto, name='eliminarArtefacto'),

]