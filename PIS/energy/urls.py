
from django.urls import path
<<<<<<< HEAD

from .metodoList.metodoListInventario.inventario import eliminar_inventario, eliminar_artefacto_inventario
from .metodoList.metodoListArtefactos.artefacto import eliminar_artefacto
from .views import home, registro, contactos, nosotros, pagina_usuario, inicio_sesion, cerrar_sesion, inventario, artefacto, informe, imprimir_pdf, proyecciones
from .calculadora import grafico_consumo_actual, \
    grafico_proyeccion_mensual, grafico_artefacto_list_mayor_consumo, grafico_proyeccion_semanal

urlpatterns = [
    path('', home, name="home"),
    path('login/', inicio_sesion, name="login"),
=======
from .views import home, registro, contactos, nosotros, paginaUsuario, inicioSesion, cerrarSesion, inventario, artefacto, informe, imprimirPDF, proyecciones, diagramaUML
from .calculadora import eliminarDiaEnInventario, eliminarArtefacto, eliminarInventario,graficoConsumoActual, graficoProyeccionMensual, graficoArtefactoMasUsado, graficoProyeccionSemanal
urlpatterns = [
    path('', home, name="home"),
    path('login/', inicioSesion, name="login"),
    path('diagramaUML/', diagramaUML, name='diagramaUML'),
>>>>>>> 9f62899f56696220cb6f2fc053cbf59d998e8360
    path('registro/', registro, name="registro"),
    path('contactos/', contactos, name="contactos"),
    path('nosotros/', nosotros, name="nosotros"),
    path('paginaUsuario/', pagina_usuario, name="paginaUsuario"),
    path('c', cerrar_sesion, name="cerrarSesion"),
    path('paginaUsuario/inventario/', inventario, name="inventario"),
    path('paginaUsuario/inventario/<int:inventario_id>/', eliminar_artefacto_inventario, name='eliminarArtefactoInventario'),
    path('paginaUsuario/inventario/eliminarInventario/', eliminar_inventario, name='eliminarInventario'),
    path('paginaUsuario/inventario/artefactos/', artefacto, name="artefacto"),
    path('paginaUsuario/inventario/artefactos/<int:artefacto_id>/', eliminar_artefacto, name='eliminarArtefacto'),
    path('paginaUsuario/inventario/informe/', informe, name="informe"),
    path('paginaUsuario/inventario/informe/pdf', imprimir_pdf, name="imprimirPDF"),
    path('paginaUsuario/proyecciones/', proyecciones, name="proyecciones"),
    path('paginaUsuario/proyecciones/graficoConsumoActual', grafico_consumo_actual, name="graficoConsumoActual"),
    path('paginaUsuario/proyecciones/graficoProyeccionSemanal', grafico_proyeccion_semanal, name="grafico_proyeccion_semanal"),
    path('paginaUsuario/proyecciones/graficoProyeccionMensual', grafico_proyeccion_mensual, name="grafico_proyeccion_semanal"),
    path('paginaUsuario/proyecciones/graficoArtefactoMasUsado', grafico_artefacto_list_mayor_consumo, name="grafico_proyeccion_semanal"),

]