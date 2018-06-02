from django import forms
from dal import autocomplete
from .models import *

class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ('descripcion',)

class ProductoProduccionForm(forms.ModelForm):
    class Meta:
        model = ProductoProduccion
        fields = ('produccion', 'producto_para_producir', 'cantidad_para_producir', 'producto_producido', 'cantidad_producido')
        widgets = { 'produccion': forms.HiddenInput(),
                    'producto_para_producir': autocomplete.ModelSelect2('producto_autocomplete'),
                    'producto_producido': autocomplete.ModelSelect2('producto_autocomplete')}

    def clean(self):
        data = super().clean()
        if data.get('producto_para_producir').id == data.get('producto_producido').id:
            raise forms.ValidationError("Los productos son iguales")
        producto = Producto.objects.get(id = data.get('producto_para_producir').id)
        if producto.stock < data.get('cantidad_para_producir'):
             raise forms.ValidationError(
                    "Stock insuficiente. Disponible: " + str(producto.stock) )
