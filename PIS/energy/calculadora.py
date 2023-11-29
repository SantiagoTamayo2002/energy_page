from datetime import datetime

import sympy as sym
from django.db.models import Sum
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
import numpy as np
from .models import Artefactos, Inventario, ConsumoDiarioMensual


def calcularConsumoTotal(consumoTotalPorArtefacto, cantidadArtefactos, horasDeUso):
    consumoTotal = (consumoTotalPorArtefacto * cantidadArtefactos * horasDeUso).__round__(2)
    return consumoTotal

def calcularConsumoTotalMensual(user):
    mesActual = datetime.now().month
    consumoMensual = ConsumoDiarioMensual.objects.filter(user=user, dia__month=mesActual).aggregate(Sum('consumoTotal'))['consumoTotal__sum'] or 0
    return consumoMensual

def eliminarArtefacto(request, artefacto_id):
    artefacto = Artefactos.objects.get(pk=artefacto_id)
    artefacto.delete()
    return redirect('artefacto')



def eliminarDiaEnInventario(request, inventario_id):
    try:
        inventario = Inventario.objects.get(pk=inventario_id)
    except Inventario.DoesNotExist:
        raise Http404("El Inventario no existe")
    # Guardar el día antes de eliminar el inventario
    dia_eliminado = inventario.dia
    inventario.delete()
    # Actualizar el consumo diario mensual para el día eliminado
    total = calcularConsumoTotalMensual(request.user)
    ConsumoDiarioMensual.actualizarConsumoDiario(request.user, dia_eliminado, total)
    return redirect('inventario')


def graficoConsumoDiario(request):
    if request.user.is_authenticated:
        consumo = []
        dia = []
        counter = 0
        for i in ConsumoDiarioMensual.objects.filter(user=request.user):
            consumo.append(i.consumoTotal)
            dia.append((counter + 1).__str__())
            counter += 1

        return baseProyeccion(consumo, dia)
    else:
        return render(request, 'energy/home/paginaUsuario.html')



#Grafico de proyeccion



def graficoProyeccion(request):
    if request.user.is_authenticated:
        consumo = []
        dia = []
        counter = 0
        for i in ConsumoDiarioMensual.objects.filter(user=request.user):
            dia.append(counter + 1)
            consumo.append(i)
            counter += 1

        resultado_actual = obtenerPolinomio(request)
        funcion = resultado_actual['funcion_polinomio']
        variable = sym.Symbol('x')

        for i in range(dia.__len__()):
            consumo[i] = round(funcion(dia[i]), 2)
        dia.__str__()
        return baseProyeccion(consumo, dia)





def obtenerPolinomio(request):

    consumo = []
    dias = []
    counter = 0
    funciondelPolinomio = 0
    r2_porcentaje = 0
    ym = 0
    r2 = 0
    funcion_polinomio = 0
    grado_del_polinomio = 0
    fx = 0

    for i in ConsumoDiarioMensual.objects.filter(user=request.user):
        consumo.append(i.consumoTotal)
        dias.append(counter + 1)
        counter += 1

    for grado_del_polinomio in range(10):
        # PROCEDIMIENTO
        dias = np.array(dias)
        consumo = np.array(consumo)

        # Llenar matriz A y vector B
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
            variable = sym.Symbol('x')
            funcion_polinomio = sum(coeficiente[i] * (variable ** i) for i in range(len(coeficiente)))

            # Errores
            ym = np.mean(consumo)
            fx = sym.lambdify(variable, funcion_polinomio)
            sr = np.sum((consumo - fx(dias)) ** 2)
            st = np.sum((consumo - ym) ** 2)

            # Coeficiente de determinacion
            r2 = (st - sr) / st
            r2_porcentaje = np.around(r2 * 100, 2)

            if r2_porcentaje >= 100 or r2_porcentaje >= 95 or r2_porcentaje >= 90:
                break

        except np.linalg.LinAlgError:
            # La matriz A es singular, manejar la excepción según sea necesario
            break

        # SALIDA
    # SALIDA
    print('------------------------\n Tabla de datos')
    print('--------------------------------------')
    print(f'ymedia = {ym}\n')
    print(f'f = {funcion_polinomio}\n')
    print(f'coef_determinacion r2 = {r2}\n')
    print(str(r2_porcentaje) + '% de los datos se describe con el modelo')
    print('--------------------------------------')

    resultado_actual = {
        'dias': dias,
        'ymedia': float(ym),
        'funcion_polinomioStr': str(funcion_polinomio),
        'funcion_polinomio': fx,
        'coef_determinacion_r2': float(r2),
        'porcentaje_datos_modelo': float(r2_porcentaje),
    }

    return resultado_actual


def baseProyeccion(consumo, dia):
    proyeccion = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross',
                'label': {
                    'backgroundColor': '#455A64',  # Color del fondo del tooltip
                    'color': 'white',  # Color del texto del tooltip
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
                        'color': 'white',  # Color de la línea
                    }
                },
                'name': 'Días del Mes',  # Título del eje x
                'nameTextStyle': {
                    'fontSize': 12,
                    'color': 'white',  # Color del texto
                },
                'nameGap': 27,  # Espacio entre el nombre y el eje
                'nameLocation': 'middle',  # Ubicación del nombre del eje ('start', 'middle', 'end')
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
                        'color': 'white',  # Color de la línea
                    }
                },
                'axisLabel': {
                    'backgroundColor': 'black',
                    'color': 'white'  # Color del texto
                },
                'name': 'Consumo (kWh)',  # Título del eje y
                'textStyle': {
                    'nameGap': 20, 'nameLocation': 'middle', 'boundaryGap': False,
                },
                'nameTextStyle': {
                    'fontSize': 12,
                    'color': 'white',  # Color del texto
                },

            }
        ],
        'title': {
            'left': 'center',
            'padding': 6,
            'top': 5,
            'text': 'Prediccion del Consumo de Energía',
            'textStyle': {
                'color': 'white',  # Color del texto del título
                'fontSize': 16,  # Tamaño del texto del título
            },
        },
        'series': [
            {

                'name': 'Consumo',
                'smooth': True,
                'data': consumo,
                'itemStyle': {
                    'color': 'red',
                    'borderColor': 'white',
                    'borderWidth': 2,
                    'shadowColor': 'rgba(0, 0, 0, 0.5)',
                },
                'type': 'line',
                'lineStyle': {
                    'width': 6,  # Ancho de la línea
                    'color': '#0000FF',
                    'shadowColor': 'rgba(0, 0, 0, 0.5)',
                },
                "areaStyle": {
                    "color": {
                        "type": "linear",

                        "y2": 1,
                        "colorStops": [
                            {
                                "offset": 0,
                                "color": "rgb(255, 158, 68)"
                            },
                            {
                                "offset": 1,
                                "color": "rgb(255, 70, 131)"
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
                    "color": "black",
                    "borderColor": "orange"
                },
                "emphasis": {
                    "borderColor": "white"
                }
            },
            "showTitle": True,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": False},
                "magicType": {
                    "side": "top",
                    "show": True,
                    "type": ["line", "bar", "stack"],
                    "title": {
                        "data": "Vista de datos",
                        "line": "Linea",
                        "bar": "Barra",
                        "stack": "Apilado",
                    },
                    "iconStyle": {
                        "fontSize": 20 #Ajusta el tamaño del texto de los botones,
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
                        "fontSize": 16, # Ajusta el tamaño del texto del botón "Restaurar",
                        "size": 20,
                    }
                },
                "saveAsImage": {
                    "title": {
                        "saveAsImage": "Guardar Imagen",
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
        'backgroundColor': 'black',
    }

    return JsonResponse(proyeccion)





def gArtefactoMasUsado(request):

    diccionario = [
        ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
        ['Milk Tea', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
        ['Matcha Latte', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7],
        ['Cheese Cocoa', 40.1, 62.2, 69.5, 36.4, 45.2, 32.5],
        ['Walnut Brownie', 25.2, 37.1, 41.2, 18, 33.9, 49.1],
        ['Cheese Brownie', 16.2, 32.1, 14.1, 9.6, 12.4, 35.1],
        ['Matcha Cocoa', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Tea', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Coffee', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Milk', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Cocoa', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Brownie', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Latte', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
        ['Tea', 6.4, 18.1, 8.7, 70.1, 53.4, 85.1],
    ]
    grafica = {
        'legend': {},
        'tooltip': {
            'trigger': 'axis',
            'showContent': False,
        },
        'dataset': {
            'source': diccionario
        },
        'xAxis': {'type': 'category'},
        'yAxis': {'gridIndex': 0},
        'grid': {
            'containLabel': True,
            'margin': 100,
            'top': '70%',  # Ajusta la posición del gráfico principal ('line')
            'bottom': '0%',  # Ajusta la posición del gráfico circular ('pie')
        },
        'series': [
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
                'center': ['50%', '33%'],  # Ajusta la posición del gráfico circular ('pie')
                'emphasis': {'focus': 'self'},
                'label': {
                    'formatter': '{b}: {@2023} ({d}%)'
                },
            }
        ]
    }

    return JsonResponse(grafica)