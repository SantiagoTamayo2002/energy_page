
from datetime import datetime

import sympy as sym
from django.db.models import Sum
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
import numpy as np
from .models import Artefactos, Inventario, Informe


def calcularConsumoTotal(consumoTotalPorArtefacto, cantidadArtefactos, horasDeUso):
    consumoTotal = (consumoTotalPorArtefacto * cantidadArtefactos * horasDeUso).__round__(2)
    return consumoTotal

def calcularConsumoTotalMensual(usuario):
    mesActual = datetime.now().month
    consumoMensual = Informe.objects.filter(user=usuario, dia__month=mesActual).aggregate(Sum('consumoTotal'))['consumoTotal__sum'] or 0
    if consumoMensual != 0:
        consumoMensual = consumoMensual /1000
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
    Informe.actualizarConsumoDiario(request.user, dia_eliminado, total)
    return redirect('inventario')


def eliminarInventario(request):
    inventario = Inventario.objects.filter(user=request.user)
    consumo = Informe.objects.filter(user=request.user)
    consumo.delete()
    inventario.delete()
    return redirect('inventario')

def calcularConsumoPolinomio(request, dias):
    resultado_actual = obtenerPolinomio(request)
    funcion = resultado_actual['funcion_polinomio']
    consumo = []
    for i in range(dias):
        consumo.append(round(funcion(i), 2))
    return consumo

#############################No Topar

def graficoConsumoActual(request):
    if request.user.is_authenticated:
        consumo = []
        dia = []
        counter = 0
        for i in Informe.objects.filter(user=request.user):
            consumo.append(i.consumoTotal)
            dia.append((counter + 1).__str__())
            counter += 1

        return baseProyeccion(consumo, dia)
    else:
        return render(request, 'energy/home/paginaUsuario.html')


##################
def graficoProyeccionMensual(request):
    if request.user.is_authenticated:
        mes = 30
        consumo = calcularConsumoPolinomio(request, mes)
        dia = []
        counter = 0
        for i in range(mes):
            dia.append(counter + 1)
            counter += 1
        return baseProyeccion(consumo, dia)
def graficoProyeccionSemanal(request):
    if request.user.is_authenticated:
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        consumo = calcularConsumoPolinomio(request, dias.__len__())
        return baseProyeccion(consumo, dias)




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

    for i in Informe.objects.filter(user=request.user):
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
    print(f'f(x) = {funcion_polinomio.__str__()}\n')
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
                    'backgroundColor': '#1DA1F2',  # Color del fondo del tooltip
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
                        'color': '#1DA1F2',  # Color de la línea
                    }
                },
                'name': 'Días',  # Título del eje x
                'nameTextStyle': {
                    'fontSize': 12,
                    'color': 'black',  # Color del texto
                },
                'nameGap': 10,  # Espacio entre el nombreArtefacto y el eje
                'nameLocation': 'middle',  # Ubicación del nombreArtefacto del eje ('start', 'middle', 'end')
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
                        'color': '#1DA1F2',  # Color de la línea
                    }
                },
                'axisLabel': {
                    'backgroundColor': 'black',
                    'color': '#1DA1F2'  # Color del texto
                },
                'name': 'Consumo (kWh)',  # Título del eje y
                'textStyle': {
                    'nameGap': 20, 'nameLocation': 'middle', 'boundaryGap': False,
                },
                'nameTextStyle': {
                    'fontSize': 12,
                    'color': '#1DA1F2',  # Color del texto
                },
                'min': 0,  # Establecer el mínimo en 0 o en otro valor adecuado
            }
        ],
        'title': {
            'left': 'center',
            'padding': 6,
            'top': 10,
            'text': 'Consumo de Energía',
            'textStyle': {
                'color': 'white',  # Color del texto del título
                'fontSize': 25,  # Tamaño del texto del título
            },
        },
        'series': [
            {

                'name': 'Consumo',
                'smooth': True,
                'data': consumo,
                'itemStyle': {
                    'color': '#1DA1F2', # Color del título
                    'borderColor': '#1DA1F2',
                    'borderWidth': 2,
                    'shadowColor': '#1DA1F2',
                },
                'type': 'line',
                'lineStyle': {
                    'width': 3,  # Ancho de la línea
                    'color': 'white',
                },
                "areaStyle": {
                    "color": {
                        "type": "linear",

                        "y2": 1,
                        "colorStops": [
                            {
                                "offset": 0,
                                "color": "#1da0f2c2"
                            },
                            {
                                "offset": 1,
                                "color": "black"
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





def graficoArtefactoMasUsado(request):
    dias = []
    counter = 0

    for i in ConsumoDiarioMensual.objects.filter(user=request.user):
        dias.append(counter+1)
    for i in Informe.objects.filter(user=request.user):
        dias.append((counter+1).__str__())
        counter += 1
    artefactoSet = set()
    artefactoList = []

    for i in Inventario.objects.filter(user=request.user):
        if i.nombre not in artefactoSet:  # Verificar si el artefacto ya está en el conjunto
            artefactoSet.add(i.nombre)
            artefactosMasUsados = [i.nombre]
        if i.nombreArtefacto not in artefactoSet:  # Verificar si el artefacto ya está en el conjunto
            artefactoSet.add(i.nombreArtefacto)
            artefactosMasUsados = [i.nombreArtefacto] # Agregar el nombreArtefacto del artefacto a la lista
            consumoArtefacto = []
            for j in Inventario.objects.filter(user=request.user, nombreArtefacto=i.nombreArtefacto):
                consumoArtefacto.append(j.consumoTotal)
            artefactosMasUsados.extend(consumoArtefacto)
            artefactoList.append(artefactosMasUsados)
    artefactoList.sort(key=lambda x: sum(x[1:]), reverse=True)
    # artefactoList = [
    #     ['Dias'] + dia,
    #     ['Lavadora', 10, 20, 30, 40, 50, 51],
    #     ['Nevera', 20, 30, 45, 50],
    #     ['Televisor', 30, 40, 50, 60],
    #     ['Computadora', 40, 50, 60],
    #     ['Microondas', 50, 60, 70],
    # ]
    # print(lista)
    print(artefactoList)

    grafica = {
        'max_width': '100%',
        'max_height': '100%',
        'backgroundColor': 'black',

        'title': {
            'left': 'center',
            'text': 'Artefactos mas usados',
            'padding': 10,
            'margin': 0,
            'textStyle': {
                'color': 'white',
                'fontSize': 25,
                'fontWeight': 'bold'
            },
        },
        'legend': {

            'top': 50,
            'itemGap': 11,   # Ajusta el espacio entre el circulo
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
            'source': artefactoList,
            'properties': {
                'pading': 60,
            }
        },
        'xAxis': {
            'type': 'category',
            'data': dias,
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