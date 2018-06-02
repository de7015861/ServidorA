from django import forms
from dal import autocomplete
from .models import *

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ('descripcion',)

class ProductoEntradaForm(forms.ModelForm):
    class Meta:
        model = ProductoEntrada
        fields = ('entrada', 'producto', 'cantidad')
        widgets = { 'entrada': forms.HiddenInput(),
                    'producto': autocomplete.ModelSelect2('producto_autocomplete')}
