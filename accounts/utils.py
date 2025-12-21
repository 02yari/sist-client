from django.shortcuts import redirect
from django.urls import reverse
from clientes.models import Profile

def redirect_por_rol(user):
    # No autenticado
    if not user.is_authenticated:
        return redirect('login')

    # Superusuario → admin
    if user.is_superuser:
        return redirect('/admin/')

    # Grupos
    if user.groups.filter(name='Administrador').exists():
        return redirect('/admin/')

    if user.groups.filter(name='Analista').exists():
        return redirect(reverse('predecir_churn'))

    if user.groups.filter(name='Asesor').exists():
        return redirect(reverse('chat_churn'))

    # Empresa (PROTEGIDO)
    try:
        profile = Profile.objects.get(user=user)
        if profile.empresa:
            return redirect(reverse('empresa_dashboard'))
    except Profile.DoesNotExist:
        pass

    # Fallback seguro
    return redirect('login')
