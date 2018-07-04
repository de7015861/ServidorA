from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', reporte, name="reporte"),
    url(r'^(?P<mes>[-\w]+)/(?P<año>[-\w]+)/$',ReporteMesView.as_view(), name='reporte_mes'),
]
