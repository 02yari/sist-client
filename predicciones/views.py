from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'page_title': 'Predicciones',
        'page_subtitle': 'Sistema de predicción de abandono',
    }
    return render(request, 'predicciones/index.html', context)

@login_required
def nueva_prediccion(request):
    return render(request, 'predicciones/nueva.html')

@login_required
def historial(request):
    return render(request, 'predicciones/historial.html')

@login_required
def resultado(request, id):
    context = {'prediccion_id': id}
    return render(request, 'predicciones/resultado.html', context)

@login_required
def analizar(request):
    return render(request, 'predicciones/analizar.html')