from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artefactos, Inventario

class ArtefactosForm(forms.ModelForm):
    class Meta:
        model = Artefactos

        fields = ('nombreArtefacto', 'consumoKwH', 'horasDeUso')

        widgets = {
            'nombreArtefacto': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre del Artefacto'
                }
            ),
            'consumoKwH': forms.NumberInput(
                attrs={
                    'placeholder': 'Consumo en KwH'
                }
            ),
            'horasDeUso': forms.NumberInput(
                attrs={
                    'placeholder': 'Horas de uso'
                }
            )
        }

        labels = {
            'nombreArtefacto': 'Nombre del Artefacto',
            'consumoKwH': 'Consumo en KwH',
            'horasDeUso': 'Horas de uso',
        }







class InventarioForm(forms.ModelForm):
    artefactos = forms.ModelChoiceField(
        widget=forms.Select(attrs={'placeholder': 'Artefactos'}),
        queryset=Artefactos.objects.all(),  # Inicialmente todos los artefactos, se actualizará en el __init__
        empty_label='Seleccione un Artefacto',
        required=True,
    )

    class Meta:
        model = Inventario
        fields = ('artefactos', 'cantidadArtefactos')

        widgets = {
            'cantidadArtefactos': forms.NumberInput(attrs={'placeholder': 'Cantidad de Artefactos'}),
        }

        labels = {
            'artefactos': 'Artefacto',
            'cantidadArtefactos': 'Cantidad de Artefactos',
        }

    def __init__(self, user, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['artefactos'].queryset = Artefactos.objects.filter(user=user)


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