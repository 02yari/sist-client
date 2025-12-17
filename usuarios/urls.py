from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.index, name='index'),
    path('lista/', views.lista_usuarios, name='lista'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('permisos/', views.permisos, name='permisos'),
]