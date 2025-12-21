from django.urls import path
from .views import predecir_churn, chat_churn
from . import views

urlpatterns = [
    path("predecir/", predecir_churn, name="predecir_churn"),
    path("chat/", chat_churn, name="chat_churn"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("", views.dashboard, name="dashboard"),
    path("subir/", views.subir_clientes, name="subir_clientes"),
    path('subir-clientes/', views.subir_clientes, name='subir_clientes'),

    
]
