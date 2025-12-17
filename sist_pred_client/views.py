from django.shortcuts import render


def custom_permission_denied(request, exception=None):
    return render(request, 'usuarios/usuario_list.html', status=403)
