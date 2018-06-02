import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class ProduccionTable(tables.Table):
    referencia = tables.LinkColumn('produccion_detalle', args=[A('pk')])
    class Meta:
        model = Produccion
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['referencia', 'descripcion', 'fecha_creacion', 'estado','acciones']

class ProductoProduccionTable(tables.Table):
    class Meta:
        model = ProductoProduccion
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['producto_para_producir', 'cantidad_para_producir', 'producto_producido', 'cantidad_producido','acciones']

class ProductoProducirTableDetail(tables.Table):
    produccion = tables.LinkColumn('produccion_detalle', args=[A('produccion.pk')])
    class Meta:
        model = ProductoProduccion
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['produccion', 'producto_para_producir', 'cantidad_para_producir']

class ProductoProducidoTableDetail(tables.Table):
    produccion = tables.LinkColumn('produccion_detalle', args=[A('produccion.pk')])
    class Meta:
        model = ProductoProduccion
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['produccion','producto_producido', 'cantidad_producido']
