from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
     path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('reportes/', views.reportes, name='reportes'),
]
