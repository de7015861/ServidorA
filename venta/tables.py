import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class VentaTable(tables.Table):
    referencia = tables.LinkColumn('venta_detalle', args=[A('pk')])
    class Meta:
        model = Venta
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields = ['referencia', 'cliente', 'factura','no_de_factura', 'fecha_creacion','limite_de_pago',
            'a_cuenta', 'falta', 'pagado', 'iva', 'total', 'estado', 'acciones']

class ProductoVentaTable(tables.Table):
    class Meta:
        model = ProductoVenta
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['producto', 'cantidad', 'producto.unidades', 'producto.precio_de_venta', 'acciones']

class ProductoVentaTableDetail(tables.Table):
    venta = tables.LinkColumn('venta_detalle', args=[A('venta.pk')])
    class Meta:
        model = ProductoVenta
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['venta', 'producto', 'cantidad', 'producto.unidades', 'producto.precio_de_venta']

class PagoVentaTable(tables.Table):
    class Meta:
        model = PagoVenta
        attrs = {'class': 'table table-striped'}
        orderable = False
        fields = ['pago', 'fecha_de_pago', 'acciones']
