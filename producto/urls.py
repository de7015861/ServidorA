from django.conf.urls import url
from .autocomplete import *
from .views import *


urlpatterns = [
    url(r'^$', ProductoList.as_view(), name="producto"),
    url(r'^añadir/$', ProductoCreate.as_view(), name="producto_añadir"),
    url(r'^autocomplete/$',ProductoAutocomplete.as_view(), name='producto_autocomplete'),
    url(r'^(?P<pk>[-\w]+)/detalle/$',ProductoDetailView.as_view(), name='producto_detail'),
    url(r'^(?P<pk>[-\w]+)/update/$',ProductoUpdate.as_view(), name='producto_update'),
    url(r'^(?P<pk>[-\w]+)/eliminar/$',ProductoDelete.as_view(), name='producto_eliminar'),
]
