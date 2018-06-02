from dal.autocomplete import Select2QuerySetView
from django.db.models import Q
from .models import *

class ProductoAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = Producto.objects.all()
        if self.q:
            qset = (
                Q(producto__icontains=self.q) |
                Q(detalles__icontains=self.q) |
                Q(codigo_de_barras__icontains=self.q)
            )
            print(qset)
            qs = qs.filter(qset).distinct()
        return qs
