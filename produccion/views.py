from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
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
class ProduccionList(SingleTableView):#añadir query
    model = Produccion
    table_class = ProduccionTable
    template_name = "tabla.html"
    paginate_by = 8

    def get_queryset(self):
        qs = super(ProduccionList, self).get_queryset()
        query = self.request.GET.get('busqueda')
        if query:
            print
            try:
                qset = (Q(id__icontains=int(query[1:7])))
                print(qset)
            except:
                pass
            qset = (
                    Q(descripcion__icontains=query)|
                    Q(id__icontains=query)
                    )
            qs = qs.filter(qset).distinct()
            print(qset)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProduccionList, self).get_context_data(**kwargs)
        context['titulo'] = 'Produccion'
        context['agregar'] = True
        context['url'] = reverse_lazy('produccion_añadir')
        return context


class ProduccionCreate(CreateView):
    model = Produccion
    form_class = ProduccionForm
    success_url = reverse_lazy('produccion')#crear url para acceder a la entrada
    template_name = 'crear.html'

    def get_context_data(self, **kwargs):
        context = super(ProduccionCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar Produccion'
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProduccionUpdate(UpdateView):
    model = Produccion
    form_class = ProduccionForm
    template_name = 'crear.html'
    success_url = reverse_lazy('produccion')

    def get_context_data(self, **kwargs):
        context = super(ProduccionUpdate, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar produccion: '
        context['quitarbuscador'] = True
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProduccionDelete(DeleteView):
    model = Produccion
    success_url = reverse_lazy('produccion')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(ProduccionDelete, self).get_context_data(**kwargs)
        context['url'] = reverse_lazy('produccion')
        context['titulo'] = 'Estas seguro que deseas eliminar "' +str(self.object) + '" y todos los datos relacionados'
        context['quitarbuscador'] = True
        return context


class ProductoProduccionCreate(CreateView):
    model = ProductoProduccion
    form_class = ProductoProduccionForm
    titulo = 'Agregar producto a Produccion'
    template_name = 'creartabla.html'

    def get_context_data(self, **kwargs):
        context = super(ProductoProduccionCreate, self).get_context_data(**kwargs)
        valor = self.kwargs.get('pk')
        context['titulo'] = 'Productos en '
        context['registro'] = Produccion.objects.get(pk = valor)
        context['table'] = ProductoProduccionTable(ProductoProduccion.objects.filter(produccion__pk = valor))
        context['validar'] =  reverse_lazy('produccion_validar', args = (self.kwargs.get('pk'),))
        context['modalprocesar'] =  reverse_lazy('produccion_procesar', args = (self.kwargs.get('pk'),))
        context['modalboton'] =  "Validar"
        context['modaltitulo'] = "Validar"
        context['modaltexto'] =  "Desea validar la produccion "
        context['modalboton'] =  "Validar"
        context['quitarbuscador'] = True
        return context

    def get_initial(self, **kwargs):
        # Get the initial dictionary from the superclass method
        initial = super(ProductoProduccionCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['produccion'] = self.kwargs.get('pk')
        return initial

    def get_success_url(self, **kwargs):
        return reverse_lazy('produccion_detalle', args = (self.kwargs.get('pk'),))

class ProductoProduccionDelete(RedirectView):
    pattern_name = 'entrada-detalle'

    def get_redirect_url(self, *args, **kwargs):
        productoproduccion = ProductoProduccion.objects.get(pk=self.kwargs.get('pk'))
        page = reverse_lazy('produccion_detalle', args = (productoproduccion.produccion.pk,))
        productoproduccion.delete()
        #super().get_redirect_url(*args, **kwargs)
        return page


class ProduccionValidar(RedirectView):
    pattern_name = 'entrada-detalle'

    def get_redirect_url(self, *args, **kwargs):
        produccion = Produccion.objects.get(pk = self.kwargs.get('pk'))
        produccion.validar = True
        produccion.save()
        return reverse_lazy('produccion_detalle', args = (self.kwargs.get('pk'),))
