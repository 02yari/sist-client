from __future__ import annotations

from datetime import timedelta
from functools import lru_cache

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
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
    ultimas_predicciones = []
    try:
        total_predicciones = Prediccion.objects.count()
        ultimas_predicciones = list(
            Prediccion.objects.all().order_by('-fecha')[:5]
        )
    except OperationalError:
        # Tablas no disponibles (p.ej. migraciones no aplicadas en esa app)
        total_predicciones = None
        ultimas_predicciones = []

    context = {
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


# Backwards-compatible alias (si ya se estaba importando en otras partes)
home = inicio

from django.shortcuts import render

def dashboard_index(request):
    return render(request, 'dashboard/index.html')
