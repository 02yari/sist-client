from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def index(request):
    context = {
        'page_title': 'Chatbot IA',
        'page_subtitle': 'Asistente virtual inteligente',
    }
    return render(request, 'chatbot/index.html', context)

@login_required
def conversacion(request):
    return render(request, 'chatbot/conversacion.html')

@login_required
def historial_chat(request):
    return render(request, 'chatbot/historial.html')

@login_required
def api_chat(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '')
        respuesta = f"Recibí tu mensaje: {mensaje}"
        return JsonResponse({'respuesta': respuesta})
    return JsonResponse({'error': 'Método no permitido'}, status=405)