from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'nombre_completo',
            'telefono',
            'rol',
            'is_active',
        ]
