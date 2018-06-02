import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class SalidaTable(tables.Table):
    referencia = tables.LinkColumn('salida_detalle', args=[A('pk')])
    class Meta:
        model = Salida
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['referencia', 'descripcion', 'fecha_creacion', 'estado','acciones']

class ProductoSalidaTable(tables.Table):
    class Meta:
        model = ProductoSalida
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['producto', 'cantidad', 'acciones']

class ProductoSalidaTableDetail(tables.Table):
    salida = tables.LinkColumn('salida_detalle', args=[A('salida.pk')])
    class Meta:
        model = ProductoSalida
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['salida', 'producto', 'cantidad']
