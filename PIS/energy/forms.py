from django import forms

from .models import Artefactos, Inventario

class ArtefactosForm(forms.ModelForm):
    class Meta:
        model = Artefactos
        fields = ('nombreArtefacto', 'consumoKwH', 'horasDeUso')

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ('artefacto', 'cantidadArtefactos', )
        artefactos = forms.ModelMultipleChoiceField(
            queryset=Artefactos.objects.all(),
            widget=forms.CheckboxSelectMultiple,
        )