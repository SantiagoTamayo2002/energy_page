from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from energy.metodoList.metodoListInventario.inventario import eliminar_inventario, eliminar_artefacto_inventario
from energy.metodoList.metodoListArtefactos.artefacto import eliminar_artefacto
from energy.views import home, registro, contacto, sobre_el_equipo, pagina_usuario, inicio_sesion, cerrar_sesion, \
    inventario, \
    artefacto, informe, imprimir_pdf, proyeccion, ubicaciones_de_usuarios, actualizar_perfil_usuario
from energy.calculadora import generar_grafico_proyeccion_consumo_actual, api_leaflet, \
    generar_grafico_proyeccion_mensual, generar_grafico_artefacto_list_mayor_consumo, generar_grafico_proyeccion_semanal
from energy.viewsets import UserViewSet, ArtefactoViewSet, UbicacionUsuarioViewSet
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register(r'Usuarios', UserViewSet, basename='user')
router.register(r'Artefactos', ArtefactoViewSet, basename='artefacto')
router.register(r'Ubicaciones_Usuarios', UbicacionUsuarioViewSet, basename='ubicacion_usuario')





urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name="home"),
    path('api/', include(router.urls)),
    path('api_leaflet/ubicaciones', api_leaflet, name="api_leaflet"),
    path('mapa_ubicaciones/', ubicaciones_de_usuarios, name="mapa_ubicaciones"),
    path('login/', inicio_sesion, name="login"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='energy/home/cambiar_contrasena.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='energy/home/contrasena_enviada.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='energy/home/cambio_nueva_contraseña.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='energy/home/contrasena_cambiada.html'), name="password_reset_complete"),
    path('registro/', registro, name="registro"),
    path('contactos/', contacto, name="contactos"),
    path('nosotros/', sobre_el_equipo, name="nosotros"),
    path('paginaUsuario/', pagina_usuario, name="paginaUsuario"),
    path('paginaUsuario/perfil/', actualizar_perfil_usuario, name="perfil"),
    path('c/', cerrar_sesion, name="cerrarSesion"),
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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)