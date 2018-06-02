from django import forms
from dal import autocomplete
from .models import *

class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        fields = ('descripcion',)

class ProductoSalidaForm(forms.ModelForm):
    class Meta:
        model = ProductoSalida
        fields = ('salida', 'producto', 'cantidad')
        widgets = { 'salida': forms.HiddenInput(),
                    'producto': autocomplete.ModelSelect2('producto_autocomplete')}

    def clean(self):
        data = super().clean()
        print(data.get('producto'))
        producto=Producto.objects.get(id = data.get('producto').id)
        if producto.stock < data.get('cantidad'):
             raise forms.ValidationError(
                    "Stock insuficiente. Disponible: " + str(producto.stock) )
