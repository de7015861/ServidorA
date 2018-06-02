from django.conf.urls import url
from .autocomplete import *
from .views import *

urlpatterns = [
    url(r'^$', ClienteList.as_view(), name="cliente"),
    url(r'^añadir/$', ClienteCreate.as_view(), name="cliente_añadir"),
    url(r'^autocomplete/$',ClienteAutocomplete.as_view(), name='cliente_autocomplete'),
    #url(r'^(?P<pk>[-\w]+)/detalle/$',ClienteDetailView.as_view(), name='cliente_detail'),
    url(r'^(?P<pk>[-\w]+)/update/$',ClienteUpdate.as_view(), name='cliente_update'),
    url(r'^(?P<pk>[-\w]+)/eliminar/$',ClienteDelete.as_view(), name='cliente_eliminar'),
]
