from django.conf.urls import url
#from .autocomplete import *
from .views import *
from reporte.views import reporteproduccion

urlpatterns = [
    url(r'^$', ProduccionList.as_view(), name="produccion"),
    url(r'^añadir/$', ProduccionCreate.as_view(), name="produccion_añadir"),
    url(r'^(?P<pk>[-\w]+)/detalle/$', ProductoProduccionCreate.as_view(), name="produccion_detalle"),
    url(r'^(?P<pk>[-\w]+)/eliminar/$', ProduccionDelete.as_view(), name="produccion_eliminar"),
    url(r'^(?P<pk>[-\w]+)/update/$',ProduccionUpdate.as_view(), name='produccion_update'),
    url(r'^(?P<pk>[-\w]+)/procesar/$', ProduccionValidar.as_view(), name="produccion_procesar"),
    url(r'^producto/(?P<pk>[-\w]+)/eliminar/$', ProductoProduccionDelete.as_view(), name="productoproduccion_eliminar"),
    url(r'^(?P<pk>[-\w]+)/reporte/$', reporteproduccion, name="produccion_reporte"),
]
