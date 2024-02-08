from rest_framework import routers
from django.urls import path, include

from .metodoList.metodoListInventario.inventario import eliminar_inventario, eliminar_artefacto_inventario
from .metodoList.metodoListArtefactos.artefacto import eliminar_artefacto
from .views import home, registro, contacto, sobre_el_equipo, pagina_usuario, inicio_sesion, cerrar_sesion, inventario, artefacto, informe, imprimir_pdf, proyeccion
from .calculadora import generar_grafico_proyeccion_consumo_actual, \
    generar_grafico_proyeccion_mensual, generar_grafico_artefacto_list_mayor_consumo, generar_grafico_proyeccion_semanal
from .viewsets import UserViewSet, ArtefactoViewSet
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'Usuarios', UserViewSet)
router.register(r'Artefactos', ArtefactoViewSet)




urlpatterns = [
    path('', home, name="home"),
    path('rout/', include(router.urls)),
    path('rout/api/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', inicio_sesion, name="login"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='energy/home/cambiar_contrasena.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='energy/home/contrasena_enviada.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='energy/home/nueva_contrasena.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='energy/home/contrasena_cambiada.html'), name="password_reset_complete"),

    path('registro/', registro, name="registro"),
    path('contactos/', contacto, name="contactos"),
    path('nosotros/', sobre_el_equipo, name="nosotros"),
    path('paginaUsuario/', pagina_usuario, name="paginaUsuario"),
    path('c', cerrar_sesion, name="cerrarSesion"),
    path('paginaUsuario/inventario/', inventario, name="inventario"),
    path('paginaUsuario/inventario/<int:inventario_id>/', eliminar_artefacto_inventario, name='eliminarArtefactoInventario'),
    path('paginaUsuario/inventario/eliminarInventario/', eliminar_inventario, name='eliminarInventario'),
    path('paginaUsuario/inventario/artefactos/', artefacto, name="artefacto"),
    path('paginaUsuario/inventario/artefactos/<int:artefacto_id>/', eliminar_artefacto, name='eliminarArtefacto'),
    path('paginaUsuario/inventario/informe/', informe, name="informe"),
    path('paginaUsuario/inventario/informe/pdf', imprimir_pdf, name="imprimirPDF"),
    path('paginaUsuario/proyecciones/', proyeccion, name="proyecciones"),
    path('paginaUsuario/proyecciones/graficoConsumoActual', generar_grafico_proyeccion_consumo_actual, name="graficoConsumoActual"),
    path('paginaUsuario/proyecciones/graficoProyeccionSemanal', generar_grafico_proyeccion_semanal, name="grafico_proyeccion_semanal"),
    path('paginaUsuario/proyecciones/graficoProyeccionMensual', generar_grafico_proyeccion_mensual, name="grafico_proyeccion_semanal"),
    path('paginaUsuario/proyecciones/graficoArtefactoMasUsado', generar_grafico_artefacto_list_mayor_consumo, name="grafico_proyeccion_semanal"),
]