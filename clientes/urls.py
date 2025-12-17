from django.urls import path
from . import views

app_name = 'clientes'
urlpatterns = [
    path('', views.index, name='index'),  # Página principal de clientes
     path('lista/', views.lista_clientes, name='lista'),
    path('nuevo/', views.nuevo_cliente, name='nuevo'),
    path('editar/<int:id>/', views.editar_cliente, name='editar'),
    path('detalle/<int:id>/', views.detalle_cliente, name='detalle'),
    path('eliminar/<int:id>/', views.eliminar_cliente, name='eliminar'),
]