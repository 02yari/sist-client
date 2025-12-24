from django.db import models

# clientes/models.py
from django.db import models

class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_registro = models.DateField(auto_now_add=True)

    RIESGO_CHOICES = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Alto', 'Alto'),
    ]

    # Nivel de riesgo categórico (se usa para UI y reglas de negocio)
    nivel_riesgo = models.CharField(max_length=10, choices=RIESGO_CHOICES, default='Bajo')

    # Probabilidad (0..1) calculada por el modelo, útil para ordenar/filtrar
    probabilidad_abandono = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

