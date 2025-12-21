from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from clientes.models import Empresa, Profile
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login
from accounts.utils import redirect_por_rol
from clientes.models import Empresa, Profile
# ----------------------------
# Redirección según rol
# ----------------------------
def redirect_por_rol(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login'))
    if user.is_superuser or user.groups.filter(name='Administrador').exists():
        return redirect('/admin/')  # Admin default
    elif user.groups.filter(name='Analista').exists():
        return redirect(reverse('clientes:predecir'))  # Ajusta tu namespace
    elif user.groups.filter(name='Asesor').exists():
        return redirect(reverse('clientes:chat'))  # Ajusta tu namespace
    elif Profile.objects.filter(user=user, empresa__isnull=False).exists():
        return redirect(reverse('empresa_dashboard'))
# ----------------------------
# Login personalizado
# ----------------------------
class LoginPorRol(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        from django.contrib.auth import login
        login(self.request, user)
        return redirect_por_rol(user)

# ----------------------------
# Logout personalizado
# ----------------------------
class LogoutViewCustom(LogoutView):
    next_page = '/accounts/login/'

# ----------------------------
# Registro de empresa / usuario
# ----------------------------
def registro_empresa(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        nombre_empresa = request.POST.get("empresa")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
            return redirect('registro_empresa')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('registro_empresa')

        try:
            # 1️⃣ Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # 2️⃣ Crear empresa
            empresa = Empresa.objects.create(nombre=nombre_empresa)

            # 3️⃣ Asignar grupo EMPRESA
            grupo_empresa, _ = Group.objects.get_or_create(name='Empresa')
            user.groups.add(grupo_empresa)

            # 4️⃣ Crear profile SOLO aquí
            Profile.objects.create(user=user, empresa=empresa)

            messages.success(
                request,
                "Empresa registrada correctamente. Ya puedes iniciar sesión."
            )
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Error al registrar. Intenta nuevamente.")
            return redirect('registro_empresa')

    return render(request, 'accounts/registro.html')

@login_required
def empresa_dashboard(request):
    return render(request, 'accounts/empresa_dashboard.html', {'user': request.user})