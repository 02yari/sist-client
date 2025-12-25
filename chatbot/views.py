from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from clientes.models import Cliente



@login_required
def index(request):
    return render(request, 'chatbot/index.html')


@login_required
def conversacion(request):
    # Vista simple: mantiene compatibilidad con rutas definidas
    return render(request, 'chatbot/index.html')


@login_required
def historial_chat(request):
    # Si no hay persistencia, mostrar UI base con estado vacío
    return render(request, 'chatbot/index.html')


@login_required
def api_chat(request):
    mensaje = request.GET.get('mensaje', '').lower().strip()

    from clientes.models import Cliente

    # ---- NORMALIZACIÓN SIMPLE ----
    palabras = mensaje.split()

    # ---- CLIENTES TOTALES ----
    if (
        'cliente' in mensaje or 'clientes' in mensaje
    ) and (
        'cuantos' in mensaje or 'cantidad' in mensaje or 'tengo' in mensaje or 'hay' in mensaje
    ):
        total = Cliente.objects.count()
        respuesta = f"Actualmente tienes {total} clientes registrados."

    # ---- CLIENTES QUE ABANDONARON ----
    elif 'abandon' in mensaje:
        abandonos = Cliente.objects.filter(estado='inactivo').count()
        respuesta = f"{abandonos} clientes han abandonado el servicio."

    # ---- CLIENTES EN RIESGO ----
    elif 'riesgo' in mensaje:
        alto_riesgo = Cliente.objects.filter(nivel_riesgo__gte=70).count()
        respuesta = f"{alto_riesgo} clientes están en riesgo alto de abandono."

    # ---- SALUDO ----
    elif mensaje in ['hola', 'hola!', 'buenas', 'buenos dias', 'buenas tardes']:
        respuesta = "¡Hola! Puedo ayudarte con estadísticas de clientes, abandono y riesgo."

    # ---- DEFAULT ----
    else:
        respuesta = (
            "Puedo ayudarte con:\n"
            "- Cuántos clientes tienes\n"
            "- Cuántos clientes han abandonado\n"
            "- Clientes en riesgo\n"
            "- Predicciones realizadas"
        )

    return JsonResponse({'respuesta': respuesta})

# Backwards-compatible alias
home = index
