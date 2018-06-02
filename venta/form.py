from django import forms
from dal import autocomplete
from .models import *
from producto.models import *

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ('cliente', 'no_de_factura', 'factura', 'iva', )
        widgets = { 'cliente': autocomplete.ModelSelect2('cliente_autocomplete')}

class ProductoVentaForm(forms.ModelForm):
    class Meta:
        model = ProductoVenta
        fields = ('venta', 'producto', 'cantidad')
        widgets = { 'venta': forms.HiddenInput(),
                    'producto': autocomplete.ModelSelect2('producto_autocomplete')}

    def clean(self):
        data = super().clean()
        producto=Producto.objects.get(id = data.get('producto').id)
        if producto.stock < data.get('cantidad'):
             raise forms.ValidationError(
                    "Stock insuficiente. Disponible: " + str(producto.stock) )


class PagoVentaForm(forms.ModelForm):
    class Meta:
        model = PagoVenta
        fields = ('venta', 'pago')
        widgets = { 'venta': forms.HiddenInput()}

    def clean(self):
        data = super().clean()
        if data.get('venta').falta < data.get('pago'):
             raise forms.ValidationError(
                    "Pago supera la deuda. Faltan: " + str(data.get('venta').falta))
