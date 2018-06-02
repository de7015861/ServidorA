from dal.autocomplete import Select2QuerySetView
from django.db.models import Q
from .models import *

class ClienteAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Cliente.objects.all()
        if self.q:
            qset = (
                Q(nombre__icontains=self.q) |
                Q(contacto__icontains=self.q) |
                Q(razon_social__icontains=self.q) |
                Q(rfc__icontains=self.q) |
                Q(correo__icontains=self.q)
            )
            print(qset)
            qs = qs.filter(qset).distinct()
        return qs
