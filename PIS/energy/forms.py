from django import forms

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
