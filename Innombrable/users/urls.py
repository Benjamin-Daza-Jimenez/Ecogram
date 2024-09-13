from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from .views import AddFollower, RemoveFollower
from . import views

app_name = 'users'

urlpatterns = [
    path('Perfil/<slug:slug>', views.user_detail, name='user_detail'),
    path('InicioDeSesion/', views.login_view, name='login'),
    path('PerfilPropio/', views.profile_view, name='profile'),
    path('Perfil/<slug:slug>/seguidores/add', AddFollower.as_view(), name='add-follower'),
    path('Perfil/<slug:slug>/seguidores/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('Registro/', views.signup_view, name='signup'),
    path('Cerrar/', views.logout_view, name='logout'),
    path('Cambiar/', views.changes, name='changes'),
]