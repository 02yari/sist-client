from django.shortcuts import render

# vistas de login y logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
#vistas CRUD
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Usuario
from .forms import UsuarioForm
from .mixins import AdminRequiredMixin
from .decorators import role_required

from usuarios.models import Usuario

def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'index.html', {'usuarios': usuarios})
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        user = self.request.user
        # Si el usuario es admin, lo lleva al admin de Django
        if user.rol == 'admin':
            return reverse_lazy('admin:index')
        # Para cualquier otro usuario, lo lleva al index central
        return '/index.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')


#vistas crud
class UsuarioListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuarios_list.html'
    context_object_name = 'usuarios'


class UsuarioCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_forms.html'
    success_url = reverse_lazy('usuarios:listar')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password('12345678')   # <-- aquí Django hace hashing automáticamente
        user.save()
        return super().form_valid(form)


class UsuarioUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:listar')


class UsuarioDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    allowed_roles = ['admin']
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:listar')

@login_required
@role_required(roles=['admin'])
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')