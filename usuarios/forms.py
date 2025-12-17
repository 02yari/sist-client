from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
import re

class UsuarioForm(forms.ModelForm):
     password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Dejar vacío si no quieres cambiar la contraseña"
    )
     
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

def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Este correo ya está en uso.")
        return email

def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # Validación de contraseña segura: al menos 8 caracteres, 1 mayúscula, 1 número
            if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
                raise ValidationError(
                    "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número."
                )
        return password

def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user