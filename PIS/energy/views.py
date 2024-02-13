from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArtefactoForm, InventarioForm, CrearUsuario, FiltrarInventarioForm, FiltrarArtefactoForm
from .models import Artefacto, Inventario, Informe, UbicacionUsuario
from django.http import HttpResponse, JsonResponse
import datetime
from django.contrib import messages

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML
from .metodoList.metodoListInforme.informe import calcular_consumo_total_mensual
from .metodoList.metodoListInventario.inventario import guardar_inventario_artefacto, eliminar_inventario, eliminar_artefacto_inventario
from .metodoList.metodoListArtefactos.artefacto import guardar_artefacto, eliminar_artefacto

# Create your views here.
def home(request):
    return render(request, 'energy/home/home.html')
def contacto(request):
    return render(request, 'energy/home/contactos.html')
def sobre_el_equipo(request):
    return render(request, 'energy/home/sobre_el_equipo.html')
def pagina_usuario(request):
    if request.user.is_anonymous:
        return redirect('home')
    return render(request, 'energy/home/pagina_usuario.html')

def cerrar_sesion(request):
    return render(request, 'energy/home/home.html', {'cS': logout(request)})
def ubicaciones_de_usuarios(request):
    return render(request, 'energy/home/ubicaciones_de_usuarios.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('paginaUsuario')
    if request.method == 'GET':
        return render(request, 'energy/home/registro.html', {
            'form': CrearUsuario
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                if request.POST['latitud'] == '' or request.POST['longitud'] == '':
                    messages.warning(request, 'No se ha proporcionado la ubicación')
                    return redirect('registro')
                else:
                    user = User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['password1'], email=request.POST['email'],
                                                    first_name=request.POST['first_name'],
                                                    last_name=request.POST['last_name'])

                    user.save()
                    # obtener ubicacion
                    latitud = request.POST['latitud']
                    longitud = request.POST['longitud']

                    # Crear una instancia de UbicacionUsuario y guardarla en la base de datos
                    UbicacionUsuario.objects.create(
                        user=user,
                        latitud=latitud,
                        longitud=longitud,
                    )
                    login(request, user)
                    return redirect('paginaUsuario')
            except IntegrityError:
                messages.warning(request, 'El usuario ya existe')
                return render(request, 'energy/home/registro.html', {
                    'form': CrearUsuario,
                })
        messages.error(request, 'Las contraseñas no coinciden')
        return render(request, 'energy/home/registro.html', {
            'form': CrearUsuario,
        })


def inicio_sesion(request):
    if request.user.is_authenticated:
        return redirect('paginaUsuario')
    if request.method == 'GET':
        return render(request, 'energy/home/inicio_sesion.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'El usuario o la contraseña no son correctos')
            return redirect('login')
        else:
            login(request, user)
            return render(request, 'energy/home/pagina_usuario.html')

def artefacto(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        artefacto = Artefacto.objects.filter(user=request.user)
        if request.method == 'GET':
            form = ArtefactoForm()
            artefacto = artefacto.order_by('nombre_artefacto')
            paginacion_artefacto = Paginator(artefacto, 5)
            numero_pagina = request.GET.get('page')
            artefacto = paginacion_artefacto.get_page(numero_pagina)
            return render(request, 'energy/home/artefacto.html', {
                'form': form,
                'artefacto': artefacto,
                'filtrar_artefacto': FiltrarArtefactoForm
            })

        elif request.method == 'POST':
            if all(key in request.POST for key in
                   ['csrfmiddlewaretoken', 'nombre_artefacto', 'consumo_wh', 'horas_de_uso']):
                form = ArtefactoForm(request.POST)
                if form.is_valid():
                    guardar_artefacto(request, form)
                    return redirect('artefacto')
                else:
                    # Manejar el caso de un formulario no válido
                    return render(request, 'energy/home/artefacto.html', {
                        'form': form,
                        'artefacto': artefacto,
                    })
            if all(key in request.POST for key in ['csrfmiddlewaretoken', 'nombre_artefacto']):
                form = FiltrarArtefactoForm(request.POST)
                if form.is_valid():
                    artefacto = Artefacto.objects.filter(user=request.user, nombre_artefacto__icontains=request.POST['nombre_artefacto'])
                    return render(request, 'energy/home/artefacto.html', {
                        'form': ArtefactoForm,
                        'artefacto': artefacto,
                        'filtrar_artefacto': form
                    })
        return render(request, 'energy/home/artefacto.html', {
            'eliminar': eliminar_artefacto,
            'ver_todo': Artefacto.objects.filter(user=request.user),
            })


def inventario(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        inventario_artefacto = Inventario.objects.filter(user=request.user)
        consumo_diario_del_mes = Informe.objects.filter(user=request.user)

        if request.method == 'GET':
            form = InventarioForm(user=request.user)
            inventario_artefacto = inventario_artefacto.order_by('dia')
            paginacion_inventario = Paginator(inventario_artefacto, 10)
            numero_pagina = request.GET.get('page')
            inventario_artefacto = paginacion_inventario.get_page(numero_pagina)
            return render(request, 'energy/home/inventario.html', {
                'form': form,
                'inventario_artefacto': inventario_artefacto,
                'consumo_diario': consumo_diario_del_mes,
                'eliminar_inventario': eliminar_inventario,
                'filtrar_inventario': FiltrarInventarioForm
            })

        elif request.method == 'POST':
            print(request.POST)
            if all(key in request.POST for key in ['csrfmiddlewaretoken', 'artefacto', 'cantidad_artefacto']):
                form = InventarioForm(request.user, request.POST)
                if form.is_valid():
                    guardar_inventario_artefacto(request, form)
                    return redirect('inventario')
                else:
                    # Manejar el caso de un formulario no válido
                    return render(request, 'energy/home/inventario.html', {
                        'form': form,
                        'inventario_artefacto': inventario_artefacto,
                        'consumo_diario': consumo_diario_del_mes,
                        'eliminar_inventario': eliminar_inventario,
                    })
            if all(key in request.POST for key in ['csrfmiddlewaretoken', 'dia', 'initial-dia']):
                form = FiltrarInventarioForm(request.POST)
                if form.is_valid():
                    inventario_artefacto = Inventario.objects.filter(user=request.user, dia=request.POST['dia'])
                    return render(request, 'energy/home/inventario.html', {
                        'form': InventarioForm(user=request.user),
                        'inventario_artefacto': inventario_artefacto,
                        'consumo_diario': consumo_diario_del_mes,
                        'filtrar_inventario': form,
                        'eliminar_inventario': eliminar_inventario,
                    })
        return render(request, 'energy/home/inventario.html', {
            'eliminar': eliminar_artefacto_inventario,
            'ver_todo': Inventario.objects.filter(user=request.user),
        })



def informe(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        consumo_diario_del_mes = Informe.objects.filter(user=request.user)
        total_mensual = calcular_consumo_total_mensual(request.user)
        return render(request, 'energy/home/informe.html', {
            'consumoDiario': consumo_diario_del_mes,
            'user': request.user,
            'consumoTotalMensual': total_mensual
        })
    return render(request, 'energy/home/informe.html')



def imprimir_pdf(request):
    if request.user.is_anonymous:
        return redirect('home')
    context = {
        'consumoDiario': Informe.objects.filter(user=request.user),
        'user': request.user,
        'consumoTotalMensual': calcular_consumo_total_mensual(request.user),
    }

    html = render_to_string('energy/home/informe.html', context)
    response = HttpResponse(content_type='application/pdf')

    # Incluir la fecha actual en el nombre del archivo
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
    nombre_archivo = f"Inform_de_{request.user.username}_{fecha_actual}.pdf"

    # Sanitizar el nombre del archivo para manejar caracteres especiales
    response['Content-Disposition'] = 'filename="{}"'.format(nombre_archivo)

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response



def proyeccion(request):
    if request.user.is_anonymous:
        return redirect('home')
    if request.user.is_authenticated:
        return render(request, 'energy/home/proyeccion.html')



