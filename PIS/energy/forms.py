from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artefacto, Inventario

class ArtefactoForm(forms.ModelForm):
    class Meta:
        model = Artefacto

        fields = ('nombre_artefacto', 'consumo_wh', 'horas_de_uso')

        widgets = {
            'nombre_artefacto': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre del Artefacto'
                }
            ),
            'consumo_wh': forms.NumberInput(
                attrs={
                    'placeholder': 'Consumo en W/h'
                }
            ),
            'horas_de_uso': forms.NumberInput(
                attrs={
                    'placeholder': 'Horas de uso'
                }
            )
        }

        labels = {
            'nombre_artefacto': 'Nombre del Artefacto',
            'consumo_wh': 'Consumo en W/h',
            'horas_de_uso': 'Horas de uso',
        }







class InventarioForm(forms.ModelForm):
    artefacto = forms.ModelChoiceField(
        widget=forms.Select(attrs={'placeholder': 'Artefacto'}),
        queryset=Artefacto.objects.all(),  # Inicialmente todos los artefacto, se actualizará en el __init__
        empty_label='Seleccione un Artefacto',
        required=True,
    )

    class Meta:
        model = Inventario
        fields = ('artefacto', 'cantidad_artefacto')

        widgets = {
            'cantidad_artefacto': forms.NumberInput(attrs={'placeholder': 'Cantidad de Artefacto'}),
        }

        labels = {
            'artefacto': 'Artefacto',
            'cantidad_artefacto': 'Cantidad de Artefacto',
        }

    def __init__(self, user, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['artefacto'].queryset = Artefacto.objects.filter(user=user)


#crear usuario

class CrearUsuario(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}),
        }