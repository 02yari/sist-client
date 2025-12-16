from django.shortcuts import render

# vistas de login y logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.rol == 'admin':
            return reverse_lazy('admin:index')
        else:
            return reverse_lazy('dashboard:inicio')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')
