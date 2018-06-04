from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
class ClienteResource(resources.ModelResource):

    class Meta:
        model = Cliente
        import_id_fields = ('id',)
        fields = ('id', 'contacto', 'direccion_entrega', 'razon_social', 'rfc',
        'direccion', 'codigo_postal', 'ciudad', 'credito', 'correo', 'telefono')

class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource

admin.site.register(Cliente, ClienteAdmin)
