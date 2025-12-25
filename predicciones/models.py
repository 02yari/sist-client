from django.db import models

class Historia(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo


class Prediccion(models.Model):
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)
    valor = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.valor}"
