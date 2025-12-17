from django.urls import path
from .views import importar_clientes
from . import views
from .views import ClienteListView, ClienteUpdateView, ClienteCreateView, ClienteDeleteView

app_name = 'clientes'

urlpatterns = [
    path('importar/', importar_clientes, name='importar'),
    path('', views.clientes_list, name='listar'),
    path('crear/', views.cliente_create, name='crear'),
    path('', ClienteListView.as_view(), name='list'),
    path('editar/<int:pk>/', views.cliente_update, name='editar'),
    path('eliminar/<int:pk>/', views.cliente_delete, name='eliminar'),
    path('', views.clientes_list, name='list'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='delete'),

]