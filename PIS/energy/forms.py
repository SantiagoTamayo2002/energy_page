from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Artefacto, Inventario, ModoClaro, Perfil


class ArtefactoForm(forms.ModelForm):
    class Meta:
        model = Artefacto
        # Definir los campos del modelo que se incluirán en el formulario
        fields = ('nombre_artefacto', 'consumo_wh', 'horas_de_uso')
        # Definir los widgets para personalizar la apariencia de los campos
        widgets = {
            'nombre_artefacto': forms.TextInput(
                attrs={
                    'placeholder': '  nombre del Artefacto',

                }
            ),
            'consumo_wh': forms.NumberInput(
                attrs={
                    'placeholder': 'Consumo en Whatts cada hora',
                    'min': '1',

                }
            ),
            'horas_de_uso': forms.NumberInput(
                attrs={
                    'placeholder': 'Horas de uso del artefacto',
                    'min': '1',
                }
            )
        }
        # Definir etiquetas personalizadas para los campos
        labels = {
            'nombre_artefacto': 'Nombre del Artefacto',
            'consumo_wh': 'Consumo en W/h      ',
            'horas_de_uso': 'Horas de uso        ',
        }


class InventarioForm(forms.ModelForm):
    # Definir un campo personalizado para el formulario
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
            'min': '1',
        }
        # Filtrar el conjunto de datos basado en el usuario pasado como argumento

    def __init__(self, user, *args, **kwargs):
        super(InventarioForm, self).__init__(*args, **kwargs)
        self.fields['artefacto'].queryset = Artefacto.objects.filter(user=user)


# crear usuario

class CrearUsuario(UserCreationForm):
    # Campos personalizados para el formulario de creación de usuario
    latitud = forms.FloatField(widget=forms.HiddenInput())
    longitud = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User
        # Campos que se mostrarán en el formulario
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Nombre de Usuario', 'minlength': 5, 'maxlength': 20,
                       'pattern': '[a-zA-Z0-9]+'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'required': True}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres', 'pattern': '[a-zA-Z ]+', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos', 'pattern': '[a-zA-Z ]+', 'required': True}),
            'password1': forms.PasswordInput(
                attrs={'placeholder': 'Contraseña', 'minlength': 8, 'maxlength': 20, 'required': True}),
            'password2': forms.PasswordInput(
                attrs={'placeholder': 'Confirmar Contraseña', 'minlength': 8, 'maxlength': 20, 'required': True}),
        }



class FiltrarArtefactoForm(forms.ModelForm):
    class Meta:
        model = Artefacto
        fields = ['nombre_artefacto']
        widgets = {
            'nombre_artefacto': forms.TextInput(attrs={'placeholder': 'Buscar artefacto'}),
        }


class FiltrarInventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['dia']
        widgets = {
            'dia': forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy', 'type': 'date', 'format': 'yyyy-mm-dd'}),
        }


class ModoClaroForm(forms.ModelForm):
    class Meta:
        model = ModoClaro
        fields = ['modo_claro']
        widgets = {
            'modo_claro': forms.CheckboxInput(),
        }


class ActualizarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Nombre de Usuario', 'autofocus': True, 'minlength': 5, 'maxlength': 20,
                       'pattern': '[a-zA-Z0-9]+'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'required': True}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre', 'pattern': '[a-zA-Z ]+', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos', 'pattern': '[a-zA-Z ]+', 'required': True}),
        }


class ActualizarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'user']
        widgets = {
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
            'user': forms.HiddenInput(),
        }
