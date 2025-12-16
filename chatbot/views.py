from django.shortcuts import render

# Protección de vistas con login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, 'chatbot/inicio.html')
