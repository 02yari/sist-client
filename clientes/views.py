from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def index(request):
    context = {
        'page_title': 'Clientes',
        'page_subtitle': 'Gestión de clientes del sistema',
    }
    return render(request, 'clientes/index.html', context)

@login_required
def lista_clientes(request):
    context = {
        'page_title': 'Lista de Clientes',
        'page_subtitle': 'Todos los clientes registrados',
    }
    return render(request, 'clientes/lista.html', context)

@login_required
def nuevo_cliente(request):
    context = {
        'page_title': 'Nuevo Cliente',
        'page_subtitle': 'Agregar un nuevo cliente al sistema',
    }
    return render(request, 'clientes/nuevo.html', context)

@login_required
def editar_cliente(request, id):
    context = {
        'page_title': 'Editar Cliente',
        'page_subtitle': f'Editando cliente ID: {id}',
        'cliente_id': id,
    }
    return render(request, 'clientes/editar.html', context)

@login_required
def detalle_cliente(request, id):
    context = {
        'page_title': 'Detalle del Cliente',
        'page_subtitle': f'Información detallada del cliente',
        'cliente_id': id,
    }
    return render(request, 'clientes/detalle.html', context)

@login_required
def eliminar_cliente(request, id):
    # Esta es solo una función de ejemplo - normalmente tendría lógica de eliminación
    messages.success(request, f'Cliente {id} eliminado exitosamente')
    return redirect('clientes:index')