from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ArtefactosForm, InventarioForm
from django.views import View
from .models import Artefactos, Inventario
from django.urls import reverse
from django.http import HttpResponse

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
    return render(request,'energy/home/index.html',{'cS': logout(request)})


def registro(request):
    if request.method == 'GET':
        return render(request, 'energy/home/registro.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('paginaUsuario')
            except IntegrityError:
                return render(request, 'energy/home/registro.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'energy/home/registro.html', {
            'form': UserCreationForm,
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
            return redirect('paginaUsuario')

def artefacto(request):
    artefactos = Artefactos.objects.filter(user=request.user)
    if request.method == 'GET':
        return render(request, 'energy/home/artefactos.html', {
            'form': ArtefactosForm,
            'artefactos': artefactos
        })
    else:
        form = ArtefactosForm(request.POST)
        if form.is_valid():
            artefacto = form.save(commit=False)
            artefactoExistente = artefactos.filter(nombreArtefacto=artefacto.nombreArtefacto).exists()
            if artefactoExistente:
                return render(request, 'energy/home/artefactos.html', {
                    'form': ArtefactosForm(),
                    'artefactos': artefactos,
                    'error': 'El artefacto ya existe'
                })
            artefacto.user = request.user
            artefacto.save()
            return redirect('artefacto')

    return render(request, 'energy/home/artefactos.html', {
        'form': form,
        'artefactos': artefactos,
        'eliminar': eliminarArtefacto,
    })
def eliminarArtefacto(request, artefacto_id):
    artefacto = Artefactos.objects.get(pk=artefacto_id)
    artefacto.delete()
    return redirect('artefacto')












def inventario(request):
    if request.user.is_authenticated:
        inventarioArtefacto = Inventario.objects.all()

        if request.method == 'GET':
            return render(request, 'energy/home/inventario.html', {
                'form': InventarioForm(),
                'inventarioArtefacto': inventarioArtefacto,
            })
        elif request.method == 'POST':
            form = InventarioForm(request.POST)
            if form.is_valid():
                inventario = form.save(commit=False)
                inventario.user = request.user
                inventario.save()
                return redirect('inventario')
            else:
                # Manejar el caso de un formulario no válido
                return render(request, 'energy/home/inventario.html', {
                    'form': form,
                    'inventarioArtefacto': inventarioArtefacto,
                })
    else:
        # Manejar el caso en que el usuario no está autenticado
        return redirect('login')  # Redirigir a tu página de inicio de sesión