from __future__ import annotations

from datetime import timedelta
from functools import lru_cache

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
from django.db import models
from predicciones.models import Prediccion
from django.shortcuts import render
from django.utils import timezone

from clientes.models import Cliente


@lru_cache(maxsize=1)



@login_required
def inicio(request):
    hoy = timezone.localdate()
    desde_30_dias = hoy - timedelta(days=30)

    total_clientes = Cliente.objects.count()
    clientes_ult_30_dias = Cliente.objects.filter(fecha_registro__gte=desde_30_dias).count()

    User = get_user_model()
    total_usuarios_activos = User.objects.filter(is_active=True).count()

    total_predicciones = None
    predicciones_hoy = 0
    ultimas_predicciones = []
    try:
        total_predicciones = Prediccion.objects.count()
        predicciones_hoy = Prediccion.objects.filter(fecha_prediccion__date=hoy).count()
        ultimas_predicciones = list(
            Prediccion.objects.all().order_by('-fecha')[:5]
        )
    except OperationalError:
        # Tablas no disponibles (p.ej. migraciones no aplicadas en esa app)
        total_predicciones = None
        predicciones_hoy = 0
        ultimas_predicciones = []

    context = {
        'estadisticas': {
            'clientes_totales': total_clientes,
            'predicciones_hoy': predicciones_hoy,
        },
        'total_clientes': total_clientes,
        'total_usuarios_activos': total_usuarios_activos,
        'total_predicciones': total_predicciones,
        'ultimas_predicciones': ultimas_predicciones,
        'clientes_ult_30_dias': clientes_ult_30_dias,
        'page_title': 'Dashboard',
        'page_subtitle': 'Resumen del sistema',
    }
    return render(request, 'dashboard/inicio.html', context)


@login_required
def configuracion(request):
    return render(request, 'dashboard/configuracion.html', {'page_title': 'Configuración'})


@login_required
def ayuda(request):
    return render(request, 'dashboard/ayuda.html', {'page_title': 'Ayuda'})


@login_required
def reportes(request):
    return render(request, 'dashboard/reportes.html', {'page_title': 'Reportes'})


@login_required
def api_stats(request):
    total_clientes = Cliente.objects.count()
    total_activos = Cliente.objects.filter(estado='activo').count()
    total_inactivos = Cliente.objects.filter(estado='inactivo').count()

    riesgo_bajo = Cliente.objects.filter(nivel_riesgo='Bajo').count()
    riesgo_medio = Cliente.objects.filter(nivel_riesgo='Medio').count()
    riesgo_alto = Cliente.objects.filter(nivel_riesgo='Alto').count()

    avg_prob = Cliente.objects.all().aggregate(avg=models.Avg('probabilidad_abandono'))['avg'] or 0.0
    try:
        avg_prob = float(avg_prob)
    except (TypeError, ValueError):
        avg_prob = 0.0

    data = {
        'resumen': {
            'total_clientes': total_clientes,
            'total_activos': total_activos,
            'total_inactivos': total_inactivos,
            'probabilidad_promedio_pct': round(avg_prob * 100.0, 2),
        },
        'distribuciones': {
            'riesgo': {
                'Bajo': riesgo_bajo,
                'Medio': riesgo_medio,
                'Alto': riesgo_alto,
            },
            'estado': {
                'activo': total_activos,
                'inactivo': total_inactivos,
            },
        },
    }
    return JsonResponse(data)


# Backwards-compatible alias (si ya se estaba importando en otras partes)
home = inicio

from django.shortcuts import render

def dashboard_index(request):
    return render(request, 'dashboard/index.html')
