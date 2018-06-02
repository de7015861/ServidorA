import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class ProductoTable(tables.Table):
    producto = tables.LinkColumn('producto_detail', args=[A('pk')])
    class Meta:
        model = Producto
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ('producto', 'detalles', 'codigo_de_barras', 'tipo_del_producto',
                    'stock', 'unidades', 'costo', 'precio_de_venta', 'acciones')
