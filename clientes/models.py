from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    edad = models.IntegerField()
    antiguedad_meses = models.IntegerField()
    frecuencia_uso = models.IntegerField(help_text="Cantidad de usos del servicio por mes")
    reclamos = models.IntegerField(default=0)
    pagos_atrasados = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    empresa = models.CharField(max_length=100, default="Empresa1") 
    churn_probabilidad = models.FloatField(null=True, blank=True)
    churn_riesgo = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nombre if self.empresa else 'Sin empresa'}"
    
