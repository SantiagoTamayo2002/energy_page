from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


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


