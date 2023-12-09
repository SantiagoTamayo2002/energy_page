from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArtefactosForm, InventarioForm, CrearUsuario
from .models import Artefactos, Inventario, Informe
import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML
from .calculadora import calcularConsumoTotal, eliminarDiaEnInventario, eliminarArtefacto, calcularConsumoTotalMensual , eliminarInventario


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







def gestionarArtefato(request):
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








def gestionarInventario(request):
    if request.user.is_authenticated:
        inventarioArtefacto = Inventario.objects.filter(user=request.user)
        consumoDiarioDelMes = Informe.objects.filter(user=request.user)

        if request.method == 'GET':
            form = InventarioForm(user=request.user)
            return render(request, 'energy/home/inventario.html', {
                'form': form,
                'inventarioArtefacto': inventarioArtefacto,
                'consumoDiario': consumoDiarioDelMes,
                'eliminarInventario': eliminarInventario,
            })
        elif request.method == 'POST':
            form = InventarioForm(request.user, request.POST)
            if form.is_valid():
                inventario = form.save(commit=False)
                # Obtén el ID del artefacto desde el formulario
                artefactoid = InventarioForm(request.user, request.POST).data['artefactos']
                artefacto = Artefactos.objects.get(pk=artefactoid)

                # Verifica si ya existe un inventario para el usuario, el día y el artefacto
                if Inventario.objects.filter(user=request.user, dia=inventario.dia, nombreArtefacto=artefacto).exists():
                    return render(request, 'energy/home/inventario.html', {
                        'form': form,
                        'inventarioArtefacto': inventarioArtefacto,
                        'consumoDiario': consumoDiarioDelMes,
                        'eliminarInventario': eliminarInventario,
                        'error': 'El artefacto ya ha sido hagregado el dia de hoy, por favor si require cambiar la cantidad de su artefacto, elimine eh ingrese una nueva cantidad'
                    })
                else:
                    inventario.nombreArtefacto = artefacto.nombreArtefacto
                    inventario.horasDeUso = artefacto.horasDeUso
                    inventario.consumoArtefacto = artefacto.consumoKwH
                    inventario.consumoTotal = calcularConsumoTotal(inventario.consumoArtefacto, inventario.cantidadArtefactos, inventario.horasDeUso)
                    inventario.user = request.user
                    inventario.save()
                    ######################
                    total = calcularConsumoTotalMensual(request.user)
                    Informe.actualizarConsumoDiario(request.user, inventario.dia, total)
                ######################
                    return redirect('inventario')
            else:
                # Manejar el caso de un formulario no válido
                return render(request, 'energy/home/inventario.html', {
                    'form': form,
                    'inventarioArtefacto': inventarioArtefacto,
                    'consumoDiario': consumoDiarioDelMes,
                    'eliminarInventario': eliminarInventario,
                })
    else:
        # Manejar el caso en que el usuario no está autenticado
        return render(request, 'energy/home/inventario.html', {
            'eliminar': eliminarDiaEnInventario,
        })



def informe(request):
    if request.user.is_authenticated:
        consumoDiarioDelMes = Informe.objects.filter(user=request.user)
        totalMensual = calcularConsumoTotalMensual(request.user)
        return render(request, 'energy/home/informe.html', {
            'consumoDiario': consumoDiarioDelMes,
            'user': request.user,
            'consumoTotalMensual': totalMensual
        })
    return render(request, 'energy/home/informe.html')



def imprimirPDF(request):
    context = {
        'consumoDiario': Informe.objects.filter(user=request.user),
        'user': request.user,
        'consumoTotalMensual': calcularConsumoTotalMensual(request.user),
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



def proyecciones(request):
    if request.user.is_authenticated:
        return render(request, 'energy/home/proyecciones.html')
    else:
      return render(request, 'energy/home/paginaUsuario.html')
