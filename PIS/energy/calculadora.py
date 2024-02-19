import sympy as sym
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
import numpy as np
from .models import Inventario, Informe, UbicacionUsuario


def api_leaflet(request):
    ubicaciones = UbicacionUsuario.objects.all()
    data = []
    for ubicacion in ubicaciones:
        data.append({
            'latitud': ubicacion.latitud,
            'longitud': ubicacion.longitud,
        })
    return JsonResponse(data, safe=False)


def calcular_consumo_polinomio(request, dias):
    resultado_actual = obtener_polinomio(request)
    funcion = resultado_actual['funcion_polinomio']
    consumo = []
    for i in range(dias):
        consumo.append(round(funcion(i + 1), 2))

    return consumo


#############################No Topar

def generar_grafico_proyeccion_consumo_actual(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        consumo = []
        dia = []
        counter = 0
        for i in Informe.objects.filter(user=request.user):
            consumo.append(i.consumo_total)
            dia.append(counter + 1)
            counter += 1

        return base_grafico_proyeccion(consumo, dia, request)
    else:
        return render(request, 'energy/home/pagina_usuario.html')


##################
def generar_grafico_proyeccion_semanal(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        consumo = calcular_consumo_polinomio(request, dias.__len__())

        return base_grafico_proyeccion(consumo, dias, request)


def generar_grafico_proyeccion_mensual(request):
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


def base_grafico_proyeccion(consumo, dia, request):
    if request.user.modoclaro.modo_claro:
        backgroundColor = '#0d72b0'
        borderColor = 'black'
        color_1DA1F2 = 'black'
        colo_titulo = 'white'
        color_Linea = 'black'
        color_texto = 'white'
        color_item = 'orange'
        color_icono_border = 'black'
        color_icono = 'blue'
        color_icono_hover = 'orange'
        colorStops_1 = '#3300FF'
        colorStops_2 = 'red'
    else:
        color_item = 'orange'
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
                    'color': color_1DA1F2,  # Color del texto del tooltip
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
                    'fontSize': 12,
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
                    'fontSize': 12,
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
                'fontSize': 25,  # Tamaño del texto del título
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
                            }
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
        backgroundColor = '#0d72b0'
        color='black'
        borderColor = 'black'
        color_1DA1F2 = 'black'
        colo_titulo = 'white'
        color_Linea = 'black'
        color_texto = 'white'
        color_item = 'orange'
        color_icono_border = 'black'
        color_icono = 'blue'
        color_icono_hover = 'orange'
        colorStops_1 = '#3300FF'
        colorStops_2 = 'red'
    else:
        color_item = 'orange'
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
    # artefactoList = [
    #     ['Dias'] + dia,
    #     ['Lavadora', 10, 20, 30, 40, 50, 51],
    #     ['Nevera', 20, 30, 45, 50],
    #     ['Televisor', 30, 40, 50, 60],
    #     ['Computadora', 40, 50, 60],
    #     ['Microondas', 50, 60, 70],
    # ]
    # print(lista)
    # print(artefactoList)

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
                'fontSize': 25,
                'fontWeight': 'bold'
            },
        },
        'legend': {
            'top': 50,
            'itemGap': 10,  # Ajusta el espacio entre el circulo
            'textStyle': {
                'color': 'white',
                'fontSize': 14,
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
        'xAxis': {
            'type': 'category',
        },
        'yAxis': {'gridIndex': 0},
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
                    'color': 'white',
                    'formatter': '{b}: {@2023} ({d}%)',
                },
                'itemStyle': {
                    'borderColor': 'white',
                    'borderWidth': 1,
                },

            },
        ]
    }
    return JsonResponse(grafica)
