from django.shortcuts import render
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from .form import *
from .models import *
from .tables import *

# Create your views here.
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ClienteList(SingleTableView):
    model = Cliente
    table_class = ClienteTable
    template_name = "tabla.html"
    paginate_by = 8

    def get_queryset(self):
        qs = super(ClienteList, self).get_queryset()
        query = self.request.GET.get('busqueda')
        if query:
            qset = (
                Q(contacto__icontains=query) |
                Q(direccion_entrega__icontains=query) |
                Q(razon_social__icontains=query) |
                Q(rfc__icontains=query) |
                Q(correo__icontains=query)
            )
            qs = qs.filter(qset).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super(ClienteList, self).get_context_data(**kwargs)
        context['titulo'] = 'Clientes'
        context['agregar'] = True
        context['url'] = reverse_lazy('cliente_añadir')
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ClienteCreate(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('cliente')
    template_name = 'crear.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteCreate, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar cliente'
        context['quitarbuscador'] = True
        return context

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ClienteUpdate(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'crear.html'
    success_url = reverse_lazy('cliente')

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdate, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente: '
        context['quitarbuscador'] = True
        return context

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ClienteDelete(DeleteView):
    model = Cliente
    success_url = reverse_lazy('cliente')
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteDelete, self).get_context_data(**kwargs)
        context['url'] = reverse_lazy('cliente')
        context['titulo'] = 'Estas seguro que deseas eliminar "' +str(self.object) + '" y todos los datos relacionados'
        context['quitarbuscador'] = True
        return context
