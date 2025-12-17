from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'page_title': 'Dashboard Principal',
        'page_subtitle': 'Vista general del sistema',
        'estadisticas': {
            'clientes_totales': 1250,
            'predicciones_hoy': 42,
            'riesgo_alto': 18,
            'satisfaccion': 87.5,
        }
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def estadisticas(request):
    return render(request, 'dashboard/estadisticas.html')

@login_required
def reportes(request):
    return render(request, 'dashboard/reportes.html')