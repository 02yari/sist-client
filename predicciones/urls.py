from django.urls import path
from .views import entrenar_modelo, predecir_abandono, calcular_nivel_riesgo

urlpatterns = [
    path('entrenar-modelo/', entrenar_modelo, name='entrenar_modelo'),
    path('predecir-abandono/<int:cliente_id>/', predecir_abandono, name='predecir_abandono'),
    path('calcular-riesgo/<int:cliente_id>/', calcular_nivel_riesgo, name='calcular_riesgo'),
]
