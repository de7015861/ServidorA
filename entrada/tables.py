import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class EntradaTable(tables.Table):
    referencia = tables.LinkColumn('entrada_detalle', args=[A('pk')])
    class Meta:
        model = Entrada
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['referencia', 'descripcion', 'fecha_creacion', 'estado','acciones']

class ProductoEntradaTable(tables.Table):
    class Meta:
        model = ProductoEntrada
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['producto', 'cantidad', 'acciones']

class ProductoEntradaTableDetail(tables.Table):
    entrada = tables.LinkColumn('entrada_detalle', args=[A('entrada.pk')])
    class Meta:
        model = ProductoEntrada
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['entrada', 'producto', 'cantidad']
