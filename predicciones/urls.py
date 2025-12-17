from django.urls import path
from . import views

app_name = 'predicciones'
urlpatterns = [
    path('', views.index, name='index'),
    path('nueva/', views.nueva_prediccion, name='nueva'),
    path('historial/', views.historial, name='historial'),
    path('resultado/<int:id>/', views.resultado, name='resultado'),
    path('analizar/', views.analizar, name='analizar'),  
]