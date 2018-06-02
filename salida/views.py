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
class SalidaList(SingleTableView):#añadir query
    model = Salida
    table_class = SalidaTable
    template_name = "tabla.html"
    paginate_by = 8

    def get_queryset(self):
        qs = super(SalidaList, self).get_queryset()
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
        context = super(SalidaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Salidas'
        context['agregar'] = True
        context['url'] = reverse_lazy('salida_añadir')
        return context


class SalidaCreate(CreateView):
    model = Salida
    form_class = SalidaForm
    success_url = reverse_lazy('salida')#crear url para acceder a la entrada
    template_name = 'crear.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Salida'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SalidaUpdate(UpdateView):
    model = Salida
    form_class = SalidaForm
    template_name = 'crear.html'
    success_url = reverse_lazy('salida')

    def get_context_data(self, **kwargs):
        context = super(SalidaUpdate, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar salida: '
        context['quitarbuscador'] = True
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SalidaDelete(DeleteView):
    model = Salida
    success_url = reverse_lazy('salida')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(SalidaDelete, self).get_context_data(**kwargs)
        context['url'] = reverse_lazy('salida')
        context['titulo'] = 'Estas seguro que deseas eliminar "' +str(self.object) + '" y todos los datos relacionados'
        context['quitarbuscador'] = True
        return context


class ProductoSalidaCreate(CreateView):
    model = ProductoSalida
    form_class = ProductoSalidaForm
    titulo = 'Agregar producto a Salida'
    template_name = 'creartabla.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoSalidaCreate, self).get_context_data(**kwargs)
        valor = self.kwargs.get('pk')
        context['titulo'] = 'Productos en '
        context['registro'] = Salida.objects.get(pk = valor)
        context['table'] = ProductoSalidaTable(ProductoSalida.objects.filter(salida__pk = valor))
        context['validar'] =  reverse_lazy('salida_validar', args = (self.kwargs.get('pk'),))
        context['modalprocesar'] =  reverse_lazy('salida_procesar', args = (self.kwargs.get('pk'),))
        context['modalboton'] =  "Validar"
        context['modaltitulo'] = "Validar"
        context['modaltexto'] =  "Desea validar la salida "
        context['modalboton'] =  "Validar"
        context['quitarbuscador'] = True
        return context

    def get_initial(self, **kwargs):
        # Get the initial dictionary from the superclass method
        initial = super(ProductoSalidaCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['salida'] = self.kwargs.get('pk')
        return initial

    def get_success_url(self, **kwargs):
        return reverse_lazy('salida_detalle', args = (self.kwargs.get('pk'),))

class ProductoSalidaDelete(RedirectView):
    pattern_name = 'salida-detalle'

    def get_redirect_url(self, *args, **kwargs):
        productosalida = ProductoSalida.objects.get(pk=self.kwargs.get('pk'))
        page = reverse_lazy('salida_detalle', args = (productosalida.salida.pk,))
        productosalida.delete()
        #super().get_redirect_url(*args, **kwargs)
        return page


class SalidaValidar(RedirectView):
    pattern_name = 'entrada-detalle'

    def get_redirect_url(self, *args, **kwargs):
        salida = Salida.objects.get(pk = self.kwargs.get('pk'))
        salida.validar = True
        salida.save()
        return reverse_lazy('salida_detalle', args = (self.kwargs.get('pk'),))
