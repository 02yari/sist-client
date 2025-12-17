from django.urls import path
from .views import DashboardView
from .views import DashboardView

app_name = 'dashboard'

def inicio(request):
    return redirect('usuarios:login')

urlpatterns = [
    path('', DashboardView.as_view(), name='inicio'),
]
