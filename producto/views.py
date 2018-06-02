from django.shortcuts import render
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.db.models import Sum
from .form import *
from .models import *
from .tables import *
from entrada.tables import *
from salida.tables import *
from venta.tables import *
from produccion.tables import *
from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
from salida.models import *
from venta.models import *
from produccion.models import *

# Create your views here.
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductoList(SingleTableView):
    model = Producto
    table_class = ProductoTable
    template_name = "tabla.html"
    paginate_by = 8

    def get_queryset(self):
        qs = super(ProductoList, self).get_queryset()
        query = self.request.GET.get('busqueda')
        if query:
            qset = (
                Q(producto__icontains=query) |
                Q(detalles__icontains=query) |
                Q(codigo_de_barras__icontains=query)
            )
            qs = qs.filter(qset).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductoList, self).get_context_data(**kwargs)
        context['titulo'] = 'Productos'
        context['agregar'] = True
        context['url'] = reverse_lazy('producto_añadir')
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('producto')
    template_name = 'crear.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar un producto'
        context['quitarbuscador'] = True
        return context

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductoUpdate(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'crear.html'
    success_url = reverse_lazy('producto')

    def get_context_data(self, **kwargs):
        context = super(ProductoUpdate, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar producto: '
        context['quitarbuscador'] = True
        return context

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductoDelete(DeleteView):
    model = Producto
    success_url = reverse_lazy('producto')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoDelete, self).get_context_data(**kwargs)
        context['url'] = reverse_lazy('producto')
        context['titulo'] = 'Estas seguro que deseas eliminar "' +str(self.object) + '" y todos los datos relacionados'
        context['quitarbuscador'] = True
        return context

#Falta implementar
def cero(valor):
    return 0 if valor is None else valor

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productodetalle.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoDetailView, self).get_context_data(**kwargs)
        entradas =  ProductoEntrada.objects.filter(producto__pk=context['object'].pk)
        context['tableentradas'] = ProductoEntradaTableDetail(entradas)
        context['entradas'] = cero(entradas.aggregate(suma=Sum('cantidad'))['suma'])
        salida = ProductoSalida.objects.filter(producto__pk=context['object'].pk)
        context['tablesalidas'] = ProductoSalidaTableDetail(salida)
        context['salidas'] = cero(salida.aggregate(suma=Sum('cantidad'))['suma'])
        ventas = ProductoVenta.objects.filter(producto__pk=context['object'].pk)
        context['tableventas'] = ProductoVentaTableDetail(ventas)
        context['ventas'] = cero(ventas.aggregate(suma=Sum('cantidad'))['suma'])
        producir = ProductoProduccion.objects.filter(producto_para_producir__pk=context['object'].pk)
        context['tableproducir'] = ProductoProducirTableDetail(producir)
        context['producir'] = cero(producir.aggregate(suma=Sum('cantidad_para_producir'))['suma'])
        producido = ProductoProduccion.objects.filter(producto_producido__pk=context['object'].pk)
        context['tableproducido'] = ProductoProducidoTableDetail(producido)
        context['producido'] = cero(producido.aggregate(suma=Sum('cantidad_producido'))['suma'])
        return context
