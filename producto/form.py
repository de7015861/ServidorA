from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (  'producto', 'detalles', 'codigo_de_barras',
                    'tipo_del_producto', 'stock_minimo', 'unidades', 'costo',
                    'precio_de_venta')
