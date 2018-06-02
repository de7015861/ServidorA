import django_tables2 as tables
from django_tables2.utils import A
from .models import *

class ClienteTable(tables.Table):
    #nombre_del_producto = tables.LinkColumn('producto_detail', args=[A('pk')])
    class Meta:
        model = Cliente
        attrs = {'class': 'table table-striped responsive-table'}
        orderable = False
        fields =('contacto', 'direccion_entrega', 'razon_social',
            'rfc', 'direccion', 'codigo_postal', 'ciudad', 'credito', 'correo',
            'telefono', 'acciones')
