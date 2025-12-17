from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'page_title': 'Usuarios',
        'page_subtitle': 'Gestión de usuarios del sistema',
    }
    return render(request, 'usuarios/index.html', context)

@login_required
def lista_usuarios(request):
    return render(request, 'usuarios/lista.html')

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')

@login_required
def configuracion(request):
    return render(request, 'usuarios/configuracion.html')

@login_required
def permisos(request):
    return render(request, 'usuarios/permisos.html')