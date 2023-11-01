
from django.urls import path
from .views import home, login, registro, contactos, nosotros

urlpatterns = [
    path('', home, name= "home"),
    path('login/', login, name= "login"),
    path('registro/', registro, name= "registro"),
    path('contactos/', contactos, name= "contactos"),
    path('nosotros/', nosotros, name= "nosotros"),
]