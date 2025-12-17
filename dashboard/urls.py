from django.urls import path
from flask import redirect
from .views import DashboardView
from .views import home 

app_name = 'dashboard'

def inicio(request):
    return redirect('usuarios:login')

urlpatterns = [
    path('', DashboardView.as_view(), name='inicio'),
    path('', home, name='home'),
]
