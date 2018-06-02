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
class EntradaList(SingleTableView):#añadir query
    model = Entrada
    table_class = EntradaTable
    template_name = "tabla.html"
    paginate_by = 8

    def get_queryset(self):
        qs = super(EntradaList, self).get_queryset()
        query = self.request.GET.get('busqueda')
        if query:
            try:
                qset = (Q(id__icontains=int(query[1:7])))
            except:
                pass
            qset = (
                Q(id__icontains=query)|
                Q(descripcion__icontains=query)
                )
            qs = qs.filter(qset).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super(EntradaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Entradas'
        context['agregar'] = True
        context['url'] = reverse_lazy('entrada_añadir')
        return context


class EntradaCreate(CreateView):
    model = Entrada
    form_class = EntradaForm
    success_url = reverse_lazy('entrada')#crear url para acceder a la entrada
    template_name = 'crear.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Entrada'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EntradaUpdate(UpdateView):
    model = Entrada
    form_class = EntradaForm
    template_name = 'crear.html'
    success_url = reverse_lazy('entrada')

    def get_context_data(self, **kwargs):
        context = super(EntradaUpdate, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar producto: '
        context['quitarbuscador'] = True
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EntradaDelete(DeleteView):
    model = Entrada
    success_url = reverse_lazy('entrada')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(EntradaDelete, self).get_context_data(**kwargs)
        context['url'] = reverse_lazy('entrada')
        context['titulo'] = 'Estas seguro que deseas eliminar "' +str(self.object) + '" y todos los datos relacionados'
        context['quitarbuscador'] = True
        return context


class ProductoEntradaCreate(CreateView):
    model = ProductoEntrada
    form_class = ProductoEntradaForm
    titulo = 'Agregar producto a Entrada'
    template_name = 'creartabla.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoEntradaCreate, self).get_context_data(**kwargs)
        valor = self.kwargs.get('pk')
        context['titulo'] = 'Productos en '
        context['registro'] = Entrada.objects.get(pk = valor)
        context['table'] = ProductoEntradaTable(ProductoEntrada.objects.filter(entrada__pk = valor))
        context['validar'] =  reverse_lazy('entrada_validar', args = (self.kwargs.get('pk'),))
        context['modalprocesar'] =  reverse_lazy('entrada_procesar', args = (self.kwargs.get('pk'),))
        context['modalboton'] =  "Validar"
        context['modaltitulo'] = "Validar"
        context['modaltexto'] =  "Desea validar la venta "
        context['modalboton'] =  "Validar"
        context['quitarbuscador'] = True
        return context

    def get_initial(self, **kwargs):
        # Get the initial dictionary from the superclass method
        initial = super(ProductoEntradaCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['entrada'] = self.kwargs.get('pk')
        return initial

    def get_success_url(self, **kwargs):
        return reverse_lazy('entrada_detalle', args = (self.kwargs.get('pk'),))

class ProductoEntradaDelete(RedirectView):
    pattern_name = 'entrada-detalle'

    def get_redirect_url(self, *args, **kwargs):
        productoentrada = ProductoEntrada.objects.get(pk=self.kwargs.get('pk'))
        page = reverse_lazy('entrada_detalle', args = (productoentrada.entrada.pk,))
        productoentrada.delete()
        #super().get_redirect_url(*args, **kwargs)
        return page


class EntradaValidar(RedirectView):
    pattern_name = 'entrada-detalle'

    def get_redirect_url(self, *args, **kwargs):
        entrada = Entrada.objects.get(pk = self.kwargs.get('pk'))
        entrada.validar = True
        entrada.save()
        return reverse_lazy('entrada_detalle', args = (self.kwargs.get('pk'),))
