from django.conf.urls import url
from django.contrib import admin
from .views import *
from reporte.views import reporteentrada

urlpatterns = [
    url(r'^$', EntradaList.as_view(), name="entrada"),
    url(r'^añadir/$', EntradaCreate.as_view(), name="entrada_añadir"),
    url(r'^(?P<pk>[-\w]+)/detalle/$', ProductoEntradaCreate.as_view(), name="entrada_detalle"),
    url(r'^(?P<pk>[-\w]+)/eliminar/$', EntradaDelete.as_view(), name="entrada_eliminar"),
    url(r'^(?P<pk>[-\w]+)/update/$',EntradaUpdate.as_view(), name='entrada_update'),
    url(r'^(?P<pk>[-\w]+)/procesar/$', EntradaValidar.as_view(), name="entrada_procesar"),
    url(r'^producto/(?P<pk>[-\w]+)/eliminar/$', ProductoEntradaDelete.as_view(), name="productoentrada_eliminar"),
    url(r'^(?P<pk>[-\w]+)/reporte/$', reporteentrada, name="entrada_reporte"),
]
