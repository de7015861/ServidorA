from django.conf.urls import url
from django.contrib import admin
from .views import *
from reporte.views import reporteventa

urlpatterns = [
    url(r'^$', VentaList.as_view(), name="venta"),
    url(r'^añadir/$', VentaCreate.as_view(), name="venta_añadir"),
    url(r'^(?P<pk>[-\w]+)/detalle/$', ProductoVentaCreate.as_view(), name="venta_detalle"),
    url(r'^(?P<pk>[-\w]+)/eliminar/$', VentaDelete.as_view(), name="venta_eliminar"),
    url(r'^(?P<pk>[-\w]+)/update/$',VentaUpdate.as_view(), name='venta_update'),
    url(r'^(?P<pk>[-\w]+)/procesar/$', VentaValidar.as_view(), name="venta_procesar"),
    url(r'^producto/(?P<pk>[-\w]+)/eliminar/$', ProductoVentaDelete.as_view(), name="productoventa_eliminar"),
    url(r'^(?P<pk>[-\w]+)/pago/$', PagoVentaCreate.as_view(), name="pagoventa_detalle"),
    url(r'^pago/(?P<pk>[-\w]+)/eliminar/$', PagoVentaDelete.as_view(), name="pagoventa_eliminar"),
    url(r'^(?P<pk>[-\w]+)/reporte/$',reporteventa),
]
