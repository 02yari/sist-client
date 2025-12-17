from django.urls import path
from .views import entrenar_modelo

urlpatterns = [
    path('entrenar-modelo/', entrenar_modelo, name='entrenar_modelo'),
]
