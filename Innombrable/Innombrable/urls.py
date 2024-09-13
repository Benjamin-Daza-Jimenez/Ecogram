"""Innombrable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Innombrable.views import comienzo,temasnuevos,registro,menu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.comienzo, name='comienzo'),
    path('', include('network.urls', namespace='network')),
    path('', views.temasnuevos, name='posteo'),
    path('', include('users.urls', namespace='users')),
    path('Borrar/<slug:slug>/', views.borrar, name='borrar'),
    path('Principal/', comienzo),
    path('Principal/NuevoArticulo/',temasnuevos),
    path('Principal/Registro/',registro),
    path('Menu/',menu),
    path('Ayuda/',views.ayuda, name='ayuda'),
    path('Principal/<slug:slug>/',views.detallePost, name='detalle_post'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)