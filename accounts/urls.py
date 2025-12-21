from django.urls import path
from accounts.views import LoginPorRol, registro_empresa, LogoutViewCustom, empresa_dashboard

urlpatterns = [
    path('login/', LoginPorRol.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
    path('registro/', registro_empresa, name='registro_empresa'),
    path('empresa/dashboard/', empresa_dashboard, name='empresa_dashboard'),
]
