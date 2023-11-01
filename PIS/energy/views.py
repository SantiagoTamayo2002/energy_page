from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'energy/home/index.html')

def login(request):
    return render(request, 'energy/home/login.html')

def registro(request):
    return render(request, 'energy/home/registro.html')

def contactos(request):
    return render(request, 'energy/home/contactos.html')

def nosotros(request):
    return render(request, 'energy/home/sobreNosotros.html')
