import sympy as sym
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
import numpy as np
from .models import Inventario, Informe, UbicacionUsuario

# Vista para generar datos JSON utilizados en Leaflet
def api_leaflet(request):
    # Obtener todas las ubicaciones de usuario
    ubicaciones = UbicacionUsuario.objects.all()
    data = []
    # Construir datos en formato JSON
    for ubicacion in ubicaciones:
        data.append({
            'latitud': ubicacion.latitud,
            'longitud': ubicacion.longitud,
        })
    return JsonResponse(data, safe=False)

# Función para calcular el consumo basado en un polinomio
def calcular_consumo_polinomio(request, dias):
    resultado_actual = obtener_polinomio(request)
    funcion = resultado_actual['funcion_polinomio']
    consumo = []
    for i in range(dias):
        consumo.append(round(funcion(i + 1), 2))

    return consumo


#############################No Topar
# Función para generar un gráfico de proyección de consumo actual
def generar_grafico_proyeccion_consumo_actual(request):
    # Se verifica si el usuario está autenticado
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        # Obtener datos de consumo
        consumo = []
        dia = []
        counter = 0
        for i in Informe.objects.filter(user=request.user):
            consumo.append(i.consumo_total)
            dia.append(counter + 1)
            counter += 1
        # Generar gráfico
        return base_grafico_proyeccion(consumo, dia, request)
    else:
        return render(request, 'energy/home/pagina_usuario.html')


##################
    # Función para generar un gráfico de proyección semanal
def generar_grafico_proyeccion_semanal(request):
    # Se verifica si el usuario está autenticado
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        consumo = calcular_consumo_polinomio(request, dias.__len__())

        return base_grafico_proyeccion(consumo, dias, request)

# Función para generar un gráfico de proyección mensual
def generar_grafico_proyeccion_mensual(request):
    # Se verifica si el usuario está autenticado
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        mes = 30
        consumo = calcular_consumo_polinomio(request, mes)
        dias = []
        counter = 0
        for i in range(mes):
            dias.append(counter + 1)
            counter += 1
        return base_grafico_proyeccion(consumo, dias, request)

# Función para obtener el polinomio de consumo
def obtener_polinomio(request):
    # Inicialización de variables
    consumo = []
    dias = []
    counter = 0
    r2_porcentaje = 0
    ym = 0
    r2 = 0
    grado_del_polinomio = 0
    variable = sym.Symbol('x')
    coeficiente = [0, 1]
    funcion_polinomio = sum(coeficiente[i] * (variable ** i) for i in range(len(coeficiente)))
    fx = sym.lambdify(variable, funcion_polinomio)
    # Obtener datos de consumo y días
    for i in Informe.objects.filter(user=request.user):
        consumo.append(i.consumo_total)
        dias.append(counter + 1)
        counter += 1

    # Bucle para ajustar el polinomio
    while grado_del_polinomio < 10:
        # PROCEDIMIENTO

        # Convertir listas a arrays NumPy
        dias = np.array(dias)
        consumo = np.array(consumo)

        # Llenar matriz A y vector B para el sistema de ecuaciones
        k = grado_del_polinomio + 1
        MatrizA = np.zeros(shape=(k, k), dtype=float)
        vectorB = np.zeros(k, dtype=float)

        for i in range(k):
            for j in range(i + 1):
                coeficiente = np.sum(dias ** (i + j))
                MatrizA[i, j] = coeficiente
                MatrizA[j, i] = coeficiente
            vectorB[i] = np.sum(consumo * (dias ** i))

        try:
            # Coeficientes, resolver sistema de ecuaciones
            coeficiente = np.linalg.solve(MatrizA, vectorB)

            # Polinomio
            funcion_polinomio = sum(coeficiente[i] * (variable ** i) for i in range(len(coeficiente)))

            # Errores
            ym = np.mean(consumo)
            fx = sym.lambdify(variable, funcion_polinomio)
            sr = np.sum((consumo - fx(dias)) ** 2)
            st = np.sum((consumo - ym) ** 2)

            # Coeficiente de determinación
            r2 = (st - sr) / st
            r2_porcentaje = np.around(r2 * 100, 2)

            if r2_porcentaje >= 100 or r2_porcentaje >= 95 or r2_porcentaje >= 90:
                break

        except np.linalg.LinAlgError:
            # La matriz A es singular, manejar la excepción según sea necesario
            break
        grado_del_polinomio += 1

    # SALIDA
    # Imprimir resultados
    print('------------------------\n Tabla de datos')
    print('--------------------------------------')
    print(f'ymedia = {ym}\n')
    print(f'grado del polinomio = {grado_del_polinomio + 1}\n')
    print(f'f(x) = {funcion_polinomio.__str__()}\n')
    print(f'coef_determinacion r2 = {r2}\n')
    print(str(r2_porcentaje) + '% de los datos se describe con el modelo')
    print('--------------------------------------')

    # Crear diccionario con resultados
    resultado_actual = {
        'dias': dias,
        'ymedia': float(ym),
        'funcion_polinomioStr': str(funcion_polinomio),
        'funcion_polinomio': fx,
        'coef_determinacion_r2': float(r2),
        'porcentaje_datos_modelo': float(r2_porcentaje),
    }

    return resultado_actual

# Función base para generar gráfico de proyección
def base_grafico_proyeccion(consumo, dia, request):
    # Configuración de colores basada en el modo claro o oscuro
    if request.user.modoclaro.modo_claro:
        backgroundColor = '#03588C'
        borderColor = 'black'
        color_1DA1F2 = '#ffffff'
        colo_titulo = '#03588C'
        color_Linea = '#06b1b1'
        color_texto = '#038C8C'
        color_item = '#038C8C'
        color_icono_border = '#06b1b1'
        color_icono = '#03588C'
        color_icono_hover = '#ffffff'
        colorStops_1 = '#038C8C'
        colorStops_2 = '#038C8C'
    else:
        color_item = '#1DA1F2'
        backgroundColor = 'black'
        borderColor = 'black'
        color_1DA1F2 = '#1DA1F2'
        colo_titulo = 'white'
        color_Linea = 'white'
        color_texto = 'white'
        color_icono_border = 'orange'
        color_icono = 'black'
        color_icono_hover = 'white'
        colorStops_1 = '#3300FF'
        colorStops_2 = 'black'
        

    proyeccion = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross',
                'label': {
                    'backgroundColor': color_1DA1F2,  # Color del fondo del tooltip
                    'color': color_texto,  # Color del texto del tooltip
                }
            }
        },
        'xAxis': [
            {
                'axisTick': {
                    'alignWithLabel': True
                },
                'axisLine': {
                    'lineStyle': {
                        'color': color_1DA1F2,  # Color de la línea
                    }
                },
                'name': 'Días de consumo',  # Título del eje x
                'nameTextStyle': {
                    'fontSize': 15,
                    'color': color_1DA1F2,  # Color del texto
                },
                'nameGap': 30,  # Espacio entre el nombre_artefacto y el eje
                'nameLocation': 'middle',  # Ubicación del nombre_artefacto del eje ('start', 'middle', 'end')
                'boundaryGap': False,
                'type': "category",
                'data': dia,
            }
        ],
        'yAxis': [
            {
                'type': 'value',
                'axisLine': {
                    'lineStyle': {
                        'color': color_1DA1F2,  # Color de la línea
                    }
                },
                'axisLabel': {
                    'backgroundColor': backgroundColor,
                    'color': color_1DA1F2  # Color del texto
                },
                'name': 'Consumo (W/h)',  # Título del eje y
                'textStyle': {
                    'nameGap': 20, 'nameLocation': 'middle', 'boundaryGap': False,
                },
                'nameTextStyle': {
                    'fontSize': 15,
                    'color': color_1DA1F2,  # Color del texto
                },
                'min': 0,  # Establecer el mínimo en 0 o en otro valor adecuado
            }
        ],
        'title': {
            'left': 'center',
            'padding': 6,
            # 'top': 10,
            # 'text': 'Proyección de consumo',
            'textStyle': {
                'color': colo_titulo,  # Color del texto del título
                'fontSize': 30,  # Tamaño del texto del título
            },
        },
        'series': [

            {

                'name': 'Consumo',
                'smooth': True,
                'data': consumo,
                'itemStyle': {
                    'color': color_item,  # Color del título
                    'borderColor': colorStops_1,
                    'borderWidth': 2,
                    'shadowColor': colorStops_2,
                },
                'type': 'line',
                'lineStyle': {
                    'width': 3,  # Ancho de la línea
                    'color': color_Linea,  # Color de la línea
                },
                "areaStyle": {
                    "color": {
                        "type": "linear",

                        "y2": 1,
                        "colorStops": [
                            {
                                "offset": 0,
                                "color": colorStops_1
                            },
                            {
                                "offset": 1,
                                "color": colorStops_2
                            },
                        ]
                    }
                }
            }
        ],
        "toolbox": {
            "show": True,
            "orient": "vertical",
            "margin": {
                "top": "center",
                'bottom': 'center',
                'left': 20,
            },
            "left": "right",
            "top": "center",
            "iconStyle": {
                "normal": {
                    "color": color_icono,
                    "borderColor": color_icono_border,
                },
                "emphasis": {
                    "borderColor": color_icono_hover,
                }
            },
            "showTitle": True,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": True, "title": "Datos",
                             "lang": ["Datos", "Cerrar"],
                             'textareaBorderColor': 'green',

                             },

                "magicType": {
                    "side": "top",
                    "show": True,
                    "type": ["line", "bar", "stack"],
                    "title": {
                        "data": "Datos",
                        "line": "Linea",
                        "bar": "Barra",
                        "stack": "Apilado",
                    },
                    "iconStyle": {
                        "fontSize": 20  # Ajusta el tamaño del texto de los botones,
                    },
                },
                "dataZoom": {
                    "yAxisIndex": "none",
                    "title": {
                        "zoom": "Zoom",
                        "back": "Restaurar",
                    },
                    "iconStyle": {
                        "fontSize": 16  # Ajusta el tamaño del texto del botón "Zoom",
                    }
                },
                "restore": {
                    "title": {
                        "restore": "Restaurar",
                    },
                    "iconStyle": {
                        "fontSize": 16,  # Ajusta el tamaño del texto del botón "Restaurar",
                        "size": 20,
                    }
                },
                "saveAsImage": {
                    "title": {
                        "saveAsImage": "Guardar",
                    },
                    "iconStyle": {
                        "fontSize": 16  # Ajusta el tamaño del texto del botón "Guardar como imagen",
                    }
                }
            },
        },

        'dataZoom': [
            {
                'type': 'inside',
                'start': 0,
                'end': 100,
            },
            {
                'show': True,
                'type': 'slider',
                'yAxisIndex': 'none',
                'start': 0,
                'end': 100,
            },
        ],
        'backgroundColor': backgroundColor,
    }

    return JsonResponse(proyeccion)


def generar_grafico_artefacto_list_mayor_consumo(request):
    if request.user.modoclaro.modo_claro:
        backgroundColor = '#F2F2F2'
        color='#03588C'
        colo_titulo = '#03588C'
        color_Linea = '#023E73'
        color_texto = '#023E73'
        color_item = '#023E73'
        color_icono_border = '#F2F2F2'
    else:
        color='white'
        color_item = 'white'
        backgroundColor = 'black'
        colo_titulo = 'white'
        color_Linea = 'white'
        color_texto = 'white'
        color_icono_border = 'white'

    if request.user.is_anonymous:
        return redirect('home')

    dias = []
    counter = 0

    for i in Informe.objects.filter(user=request.user):
        dias.append((counter + 1).__str__())
        counter += 1
    artefactoet = set()

    artefactoList = []
    lista = [['Dias'] + dias, ]

    for i in Inventario.objects.filter(user=request.user):
        if i.artefacto.nombre_artefacto not in artefactoet:  # Verificar si el artefacto ya está en el conjunto
            artefactoet.add(i.artefacto.nombre_artefacto)
            artefactoMasUsados = [i.artefacto.nombre_artefacto]  # Agregar el nombre_artefacto del artefacto a la lista
            consumo_artefacto = []
            for j in Inventario.objects.filter(user=request.user,
                                               artefacto__nombre_artefacto=i.artefacto.nombre_artefacto):
                consumo_artefacto.append(j.consumo_artefacto)
            artefactoMasUsados.extend(consumo_artefacto)  # Agregar el consumo del artefacto a la lista
            artefactoList.append(artefactoMasUsados)  # Agregar la lista a la lista de artefacto
    artefactoList.sort(key=lambda x: sum(x[1:]), reverse=True)
    lista.extend(artefactoList)
    print(lista)
    

    grafica = {
        'max_width': '100%',
        'max_height': '100%',
        'backgroundColor': backgroundColor,

        'title': {
            'left': 'center',
            'text': 'Artefactos con mayor consumo',
            'padding': 10,
            'margin': 0,
            'textStyle': {
                'color': color,
                'fontSize': 30,
                'fontWeight': 'bold'
            },
        },
        'legend': {
            'top': 50,
            'itemGap': 10,  # Ajusta el espacio entre el circulo
            'textStyle': {
                'color': colo_titulo,
                'fontSize': 17,
            },
        },
        'tooltip': {
            'trigger': 'axis',
            'showContent': False,
        },
        'dataset': {
            'source': lista,
            'properties': {
                'pading': 60,   
            }
        },
        'xAxis': [
            { 
                'axisTick': {
                    'alignWithLabel': True
                },
                'type': 'category',
                'axisLine': {
                     'lineStyle': {
                         'color': color_Linea,  # Color de la línea
                     }
                 },
                'name': 'Días de consumo',  # Título del eje x
                 'nameTextStyle': {
                     'fontSize': 15,
                     'color': colo_titulo,  # Color del texto
                 },
                'nameGap': 30,  # Espacio entre el nombre_artefacto y el eje
                'nameLocation': 'middle',  # Ubicación del nombre_artefacto del eje ('start', 'middle', 'end')
                'boundaryGap': False,
            }
        ],
        'yAxis': [
            { 
                'type': 'value',
                'axisLine': {
                    'lineStyle': {
                        'color': color_Linea,  # Color de la línea
                    }
                },
                'axisLabel': {
                    'color': color_item 
                },
                'name': 'Consumo (W/h)',  # Título del eje y
                'textStyle': {
                    'nameGap': 20, 'nameLocation': 'middle', 'boundaryGap': False,
                },
                'nameTextStyle': {
                    'fontSize': 15,
                    'color': color_texto,
                },
                'min': 0,
                'gridIndex': 0
            },
        ],
        'grid': {
            'position': 'top',
            'top': '60%',  # Ajusta la posición del gráfico principal ('line')
            'bottom': '15%',  # Ajusta la posición del gráfico circular ('pie')
        },  
        'series': [
            {
                'type': 'line',
                'smooth': True,
                'seriesLayoutBy': 'row',
                'emphasis': {'focus': 'series'},
            },
            {
                'type': 'line',
                'smooth': True,
                'seriesLayoutBy': 'row',
                'emphasis': {'focus': 'series'}
            },
            {
                'type': 'line',
                'smooth': True,
                'seriesLayoutBy': 'row',
                'emphasis': {'focus': 'series'}
            },
            {
                'type': 'line',
                'smooth': True,

                'seriesLayoutBy': 'row',
                'emphasis': {'focus': 'series'}
            },
            {
                'type': 'line',
                'smooth': True,
                'seriesLayoutBy': 'row',
                'emphasis': {'focus': 'series'}
            },
            {
                'type': 'line',
                'smooth': True,
                'seriesLayoutBy': 'row',
                'emphasis': {'focus': 'series'}
            },
            {
                'type': 'pie',
                'id': 'pie',
                'radius': '30%',
                'center': ['50%', '36%'],  # Ajusta la posición del gráfico circular ('pie')
                'emphasis': {'focus': 'self'},
                'label': {
                    'color': color_texto,
                    'formatter': '{b}: {@2023} ({d}%)',
                },
                'itemStyle': {
                    'borderColor': color_icono_border,
                    'borderWidth': 1,
                },
            },
        ]
    }

    return JsonResponse(grafica)
