
from django.urls import path
from .views import home, registro, contactos, nosotros, paginaUsuario, inicioSesion, cerrarSesion, inventario, artefacto, informe, imprimirPDF, proyecciones, generarGrafico
from .calculadora import eliminarDiaEnInventario, eliminarArtefacto
urlpatterns = [
    path('', home, name="home"),
    path('login/', inicioSesion, name="login"),
    path('registro/', registro, name="registro"),
    path('contactos/', contactos, name="contactos"),
    path('nosotros/', nosotros, name="nosotros"),
    path('paginaUsuario/', paginaUsuario, name="paginaUsuario"),
    path('c', cerrarSesion, name="cerrarSesion"),
    path('paginaUsuario/inventario/', inventario, name="inventario"),
    path('paginaUsuario/inventario/<int:inventario_id>/', eliminarDiaEnInventario, name='eliminarDiaEnInventario'),
    path('paginaUsuario/inventario/artefactos/', artefacto, name="artefacto"),
    path('paginaUsuario/inventario/artefactos/<int:artefacto_id>/', eliminarArtefacto, name='eliminarArtefacto'),
    path('paginaUsuario/inventario/informe/', informe, name="informe"),
    path('paginaUsuario/inventario/informe/pdf', imprimirPDF, name="imprimirPDF"),
    path('paginaUsuario/proyecciones/', proyecciones, name="proyecciones"),
    path('paginaUsuario/proyecciones/grafico', generarGrafico, name="generarGrafico"),

]