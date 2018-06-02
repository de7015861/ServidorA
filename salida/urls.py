from django.conf.urls import url
from django.contrib import admin
from .views import *
from reporte.views import reportesalida

urlpatterns = [
    url(r'^$', SalidaList.as_view(), name="salida"),
    url(r'^añadir/$', SalidaCreate.as_view(), name="salida_añadir"),
    url(r'^(?P<pk>[-\w]+)/detalle/$', ProductoSalidaCreate.as_view(), name="salida_detalle"),
    url(r'^(?P<pk>[-\w]+)/eliminar/$', SalidaDelete.as_view(), name="salida_eliminar"),
    url(r'^(?P<pk>[-\w]+)/update/$',SalidaUpdate.as_view(), name='salida_update'),
    url(r'^(?P<pk>[-\w]+)/procesar/$', SalidaValidar.as_view(), name="salida_procesar"),
    url(r'^producto/(?P<pk>[-\w]+)/eliminar/$', ProductoSalidaDelete.as_view(), name="productosalida_eliminar"),
    url(r'^(?P<pk>[-\w]+)/reporte/$', reportesalida, name="salida_reporte"),
]
