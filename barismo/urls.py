"""barismo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='producto', permanent=False)),
    url(r'^admin/', admin.site.urls),
    url(r'^producto/', include('producto.urls')),
    url(r'^entrada/', include('entrada.urls')),
    url(r'^salida/', include('salida.urls')),
    url(r'^cliente/', include('cliente.urls')),
    url(r'^venta/', include('venta.urls')),
    url(r'^produccion/', include('produccion.urls')),
    url(r'^reporte/', include('reporte.urls')),
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'producto'}, name='logout'),
]
