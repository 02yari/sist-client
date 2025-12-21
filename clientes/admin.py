from django.contrib import admin
from .models import Cliente
# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'email',
        'edad',
        'antiguedad_meses',
        'frecuencia_uso',
        'reclamos',
        'pagos_atrasados',
        'activo',
    )