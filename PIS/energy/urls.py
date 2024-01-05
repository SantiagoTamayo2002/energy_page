
from django.urls import path

from .metodoList.metodoListInventario.inventario import eliminar_inventario, eliminar_artefacto_inventario
from .metodoList.metodoListArtefactos.artefacto import eliminar_artefacto
from .views import home, registro, contacto, sobre_el_equipo, pagina_usuario, inicio_sesion, cerrar_sesion, inventario, artefacto, informe, imprimir_pdf, proyeccion
from .calculadora import generar_grafico_proyeccion_consumo_actual, \
    generar_grafico_proyeccion_mensual, generar_grafico_artefacto_list_mayor_consumo, generar_grafico_proyeccion_semanal

urlpatterns = [
    path('', home, name="home"),
    path('login/', inicio_sesion, name="login"),
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