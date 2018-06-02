from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django_tables2 import SingleTableView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from .form import *
from .models import *
from .tables import *


# Create your views here.
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class VentaList(SingleTableView):#añadir query
    model = Venta
    table_class = VentaTable
    template_name = "tabla.html"
    paginate_by = 8

    def get_queryset(self):
        qs = super(VentaList, self).get_queryset()
        query = self.request.GET.get('busqueda')
        if query:
            try:
                qset = (Q(id__icontains=int(query[1:7])))
            except:
                pass
            qset = (
                    Q(descripcion__icontains=query) |
                    Q(id__icontains=query)
                    )
            qs = qs.filter(qset).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super(VentaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Ventas'
        context['agregar'] = True
        context['url'] = reverse_lazy('venta_añadir')
        return context


class VentaCreate(CreateView):
    model = Venta
    form_class = VentaForm
    success_url = reverse_lazy('venta')#crear url para acceder a la entrada
    template_name = 'crear.html'

    def get_context_data(self, **kwargs):
        context = super(VentaCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Venta'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class VentaUpdate(UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = 'crear.html'
    success_url = reverse_lazy('venta')

    def get_context_data(self, **kwargs):
        context = super(VentaUpdate, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar venta: '
        context['quitarbuscador'] = True
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class VentaDelete(DeleteView):
    model = Venta
    success_url = reverse_lazy('venta')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(VentaDelete, self).get_context_data(**kwargs)
        context['url'] = reverse_lazy('venta')
        context['titulo'] = 'Estas seguro que deseas eliminar "' +str(self.object) + '" y todos los datos relacionados'
        context['quitarbuscador'] = True
        return context


class ProductoVentaCreate(CreateView):
    model = ProductoVenta
    form_class = ProductoVentaForm
    titulo = 'Agregar producto a Venta'
    template_name = 'creartabla.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoVentaCreate, self).get_context_data(**kwargs)
        valor = self.kwargs.get('pk')
        context['titulo'] = 'Productos en '
        context['registro'] = Venta.objects.get(pk = valor)
        context['table'] = ProductoVentaTable(ProductoVenta.objects.filter(venta__pk = valor))
        context['validar'] =  reverse_lazy('venta_validar', args = (self.kwargs.get('pk'),))
        context['modalprocesar'] =  reverse_lazy('venta_procesar', args = (self.kwargs.get('pk'),))
        context['modalboton'] =  "Validar"
        context['modaltitulo'] = "Validar"
        context['modaltexto'] =  "Desea validar la venta "
        context['modalboton'] =  "Validar"
        context['quitarbuscador'] = True
        return context

    def get_initial(self, **kwargs):
        # Get the initial dictionary from the superclass method
        initial = super(ProductoVentaCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['venta'] = self.kwargs.get('pk')
        return initial

    def get_success_url(self, **kwargs):
        return reverse_lazy('venta_detalle', args = (self.kwargs.get('pk'),))

class ProductoVentaDelete(RedirectView):
    pattern_name = 'salida-detalle'

    def get_redirect_url(self, *args, **kwargs):
        producto = ProductoVenta.objects.get(pk=self.kwargs.get('pk'))
        page = reverse_lazy('venta_detalle', args = (producto.venta.pk,))
        producto.delete()
        #super().get_redirect_url(*args, **kwargs)
        return page


class VentaValidar(RedirectView):
    pattern_name = 'entrada-detalle'

    def get_redirect_url(self, *args, **kwargs):
        venta = Venta.objects.get(pk = self.kwargs.get('pk'))
        venta.validar = True
        venta.save()
        return reverse_lazy('venta_detalle', args = (self.kwargs.get('pk'),))


class PagoVentaCreate(CreateView):
    model = PagoVenta
    form_class = PagoVentaForm
    titulo = 'Agregar pago a Venta'
    template_name = 'pago.html'

    def get_context_data(self, **kwargs):
        context = super(PagoVentaCreate, self).get_context_data(**kwargs)
        valor = self.kwargs.get('pk')
        context['titulo'] = 'Pago en '
        context['registro'] = Venta.objects.get(pk = valor)
        context['table'] = PagoVentaTable(PagoVenta.objects.filter(venta__pk = valor))
        context['quitarbuscador'] = True
        return context

    def get_initial(self, **kwargs):
        # Get the initial dictionary from the superclass method
        initial = super(PagoVentaCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['venta'] = self.kwargs.get('pk')
        return initial

    def get_success_url(self, **kwargs):
        return reverse_lazy('pagoventa_detalle', args = (self.kwargs.get('pk'),))

class PagoVentaDelete(RedirectView):
    pattern_name = 'salida-detalle'

    def get_redirect_url(self, *args, **kwargs):
        pago = PagoVenta.objects.get(pk=self.kwargs.get('pk'))
        page = reverse_lazy('pagoventa_detalle', args = (pago.venta.pk,))
        pago.delete()
        #super().get_redirect_url(*args, **kwargs)
        return page
