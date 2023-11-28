from random import randrange

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from matplotlib import pyplot as plt

from .forms import ArtefactosForm, InventarioForm, CrearUsuario
from .models import Artefactos, Inventario, ConsumoDiarioMensual
import datetime
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML
from .calculadora import calcularConsumoTotal, eliminarDiaEnInventario, eliminarArtefacto, calcularConsumoTotalMensual


# Create your views here.
def home(request):
    return render(request, 'energy/home/index.html')
def contactos(request):
    return render(request, 'energy/home/contactos.html')
def nosotros(request):
    return render(request, 'energy/home/sobreNosotros.html')
def paginaUsuario(request):
    return render(request, 'energy/home/paginaUsuario.html')

def cerrarSesion(request):
    return render(request, 'energy/home/index.html', {'cS': logout(request)})




def registro(request):
    if request.method == 'GET':
        return render(request, 'energy/home/registro.html', {
            'form': CrearUsuario
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                return redirect('paginaUsuario')
            except IntegrityError:
                return render(request, 'energy/home/registro.html', {
                    'form': CrearUsuario,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'energy/home/registro.html', {
            'form': CrearUsuario,
            'error': 'Las contraseñas no coinciden'
        })
def inicioSesion(request):
    if request.user.is_authenticated:
        return redirect('paginaUsuario')
    if request.method == 'GET':
        return render(request, 'energy/home/login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'energy/home/login.html', {
                'form': AuthenticationForm,
                'error': 'El usuario es incorrecto',
            })
        else:
            login(request, user)
            return render(request, 'energy/home/paginaUsuario.html')







def artefacto(request):
    if request.user.is_authenticated:
        artefactos = Artefactos.objects.filter(user=request.user)
        if request.method == 'GET':
            form = ArtefactosForm()
            return render(request, 'energy/home/artefactos.html', {
                'form': form,
                'artefactos': artefactos,
            })
        elif request.method == 'POST':
            form = ArtefactosForm(request.POST)
            if form.is_valid():
                artefacto = form.save(commit=False)
                #artefacto ya existe dentro del usuario
                if Artefactos.objects.filter(user=request.user, nombreArtefacto=artefacto).exists():
                    return render(request, 'energy/home/artefactos.html', {
                        'form': form,
                        'artefactos': artefactos,
                        'error': 'El artefacto ya existe',
                    })

                artefacto.user = request.user
                artefacto.save()
                return redirect('artefacto')
            else:
                # Manejar el caso de un formulario no válido
                return render(request, 'energy/home/artefactos.html', {
                    'form': form,
                    'artefactos': artefactos,
                })
    return render(request, 'energy/home/artefactos.html', {
        'eliminar': eliminarArtefacto,
        })








def inventario(request):
    if request.user.is_authenticated:
        inventarioArtefacto = Inventario.objects.filter(user=request.user)
        consumoDiarioDelMes = ConsumoDiarioMensual.objects.filter(user=request.user)

        if request.method == 'GET':
            form = InventarioForm(user=request.user)
            return render(request, 'energy/home/inventario.html', {
                'form': form,
                'inventarioArtefacto': inventarioArtefacto,
                'consumoDiario': consumoDiarioDelMes,
            })
        elif request.method == 'POST':
            form = InventarioForm(request.user, request.POST)
            if form.is_valid():
                inventario = form.save(commit=False)
                #guardar los aributos del artefacto en los atributos del inventario
                ############################
                artefactoid = InventarioForm(request.user, request.POST).data['artefactos']
                artefacto = Artefactos.objects.get(pk=artefactoid)

                ############################
                inventario.nombre = artefacto.nombreArtefacto
                inventario.horasDeUso = artefacto.horasDeUso
                inventario.consumoArtefacto = artefacto.consumoKwH
                inventario.consumoTotal = calcularConsumoTotal(inventario.consumoArtefacto, inventario.cantidadArtefactos, inventario.horasDeUso)
                inventario.user = request.user
                inventario.save()
                ######################
                total = calcularConsumoTotalMensual(request.user)
                ConsumoDiarioMensual.actualizarConsumoDiario(request.user, inventario.dia, total)
                ######################
                return redirect('inventario')
            else:
                # Manejar el caso de un formulario no válido
                return render(request, 'energy/home/inventario.html', {
                    'form': form,
                    'inventarioArtefacto': inventarioArtefacto,
                    'consumoDiario': consumoDiarioDelMes,

                })
    else:
        # Manejar el caso en que el usuario no está autenticado
        return render(request, 'energy/home/inventario.html', {
            'eliminar': eliminarDiaEnInventario,
        })



def informe(request):
    if request.user.is_authenticated:
        consumoDiarioDelMes = ConsumoDiarioMensual.objects.filter(user=request.user)
        totalMensual = calcularConsumoTotalMensual(request.user)
        return render(request, 'energy/home/informe.html', {
            'consumoDiario': consumoDiarioDelMes,
            'user': request.user,
            'consumoTotalMensual': totalMensual
        })
    return render(request, 'energy/home/informe.html')



def imprimirPDF(request):
    context = {
        'consumoDiario': ConsumoDiarioMensual.objects.filter(user=request.user),
        'user': request.user,
        'consumoTotalMensual': calcularConsumoTotalMensual(request.user),
    }

    html = render_to_string('energy/home/informe.html', context)
    response = HttpResponse(content_type='application/pdf')

    # Incluir la fecha actual en el nombre del archivo
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
    nombre_archivo = f"Inform_de_{request.user}_{fecha_actual}.pdf"

    # Sanitizar el nombre del archivo para manejar caracteres especiales
    response['Content-Disposition'] = 'filename="{}"'.format(nombre_archivo)

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response



def proyecciones(request):
    if request.user.is_authenticated:
        return render(request, 'energy/home/proyecciones.html')
    return render(request, 'energy/home/paginaUsuario.html')
def generarGrafico(request):
    if request.user.is_authenticated:
        consumo = []
        dias = []
        counter = 0
        for i in ConsumoDiarioMensual.objects.filter(user=request.user):
            consumo.append(i.consumoTotal)
            dias.append((counter+1).__str__())
            counter += 1

        grafica = {
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross',
                    'label': {
                        'backgroundColor': '#6a7985'  # Color del fondo del tooltip
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
                    'data': dias,
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
                'text': 'Consumo de Energía durente el Mes',
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
                        'width': 3,  # Ancho de la línea
                        'color': '#134DFF',
                        'shadowColor': 'rgba(0, 0, 0, 0.5)',
                    },
                    'areaStyle': {
                        'color': '#134DFF',
                        'shadowColor': '#13E9E7',
                    },
                }
            ],
            'toolbox': {
                'show': True,
                'orient': 'vertical',
                'left': 'right',
                'position': 'relative',
                'top': 'center',
                'iconStyle': {
                    'normal': {
                        'color': 'black',
                        'borderColor': 'orange',
                    },
                    'emphasis': {
                        'borderColor': 'white'
                    },
                },
                'showTitle': True,
                'feature': {
                    'mark': {'show': True},
                    'dataView': {'show': True, 'readOnly': False},
                    'magicType': {
                        'show': True,
                        'type': ['line', 'bar', 'stack'],
                        'title': {
                            'dataview': 'Vista de datos',
                            'line': 'Linea',
                            'bar': 'Barra',
                            'stack': 'Apilado',
                        },
                    },
                    'dataZoom': {
                        'yAxisIndex': 'none'
                    },
                    'restore': {},
                    'saveAsImage': {}
                },
            },
            'dataZoom': [
                {
                    'type': 'inside',
                    'start': 0,
                    'end': 100
                },
                {
                    'show': True,
                    'type': 'slider',
                    'yAxisIndex': 'none',
                    'start': 0,
                    'end': 100
                },
            ],
            'backgroundColor': 'black',
        }

        return JsonResponse(grafica)
    else:
        return render(request, 'energy/home/paginaUsuario.html')












############################################################################################

# def eliminarArtefacto(request, artefacto_id):
#     artefacto = Artefactos.objects.get(pk=artefacto_id)
#     artefacto.delete()
#     return redirect('artefacto')


# def eliminarDiaEnInventario(request, inventario_id):
#     try:
#         inventario = Inventario.objects.get(pk=inventario_id)
#     except Inventario.DoesNotExist:
#         raise Http404("El Inventario no existe")
#
#     # Guardar el día antes de eliminar el inventario
#     dia_eliminado = inventario.dia
#     inventario.delete()
#     # Actualizar el consumo diario mensual para el día eliminado
#     ConsumoDiarioMensual.actualizar_consumo_diario(request.user, dia_eliminado)
#
#     return redirect('inventario')


# def calcularConsumoTotal(consumoTotalPorArtefacto, cantidadArtefactos, horasDeUso):
#     consumoTotal = (consumoTotalPorArtefacto * cantidadArtefactos * horasDeUso).__round__(2)
#     return consumoTotal


# def imprimirPDF(request):
#     context = {
#         'consumoDiarioDelMes':  ConsumoDiarioMensual.objects.filter(user=request.user),
#         'user': request.user,
#     }
#
#     html = render_to_string('energy/home/informe.html', context)
#     response = HttpResponse(content_type='application/pdf')
#
#     # Incluir la fecha actual en el nombre del archivo
#     fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
#     nombre_archivo = f"Informe_de_{request.user}_{fecha_actual}.pdf"
#
#     # Sanitizar el nombre del archivo para manejar caracteres especiales
#     response['Content-Disposition'] = 'filename="{}"'.format(nombre_archivo)
#
#     font_config = FontConfiguration()
#     HTML(string=html).write_pdf(response, font_config=font_config)
#     return response
#calcular el consumo total del mes de del consumo total de cada dia


