from django.shortcuts import render

# Protección de vistas con login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from clientes.models import Cliente
import json

@login_required
def home(request):
    return render(request, 'chatbot/inicio.html')

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)
    pregunta = data.get("pregunta", "").lower()

    respuesta = "No entiendo tu pregunta."

    if "nivel de riesgo de" in pregunta:
        nombre_cliente = pregunta.replace("nivel de riesgo de", "").strip().title()
        try:
            cliente = Cliente.objects.get(nombre=nombre_cliente)
            respuesta = f"El nivel de riesgo de {cliente.nombre} es {cliente.nivel_riesgo}."
        except Cliente.DoesNotExist:
            respuesta = f"No encontré al cliente {nombre_cliente}."
    
    return JsonResponse({"respuesta": respuesta})
