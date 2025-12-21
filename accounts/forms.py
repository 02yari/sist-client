from django import forms
from django.contrib.auth.models import User
from clientes.models import Empresa

class RegistroEmpresaForm(forms.Form):
    nombre_empresa = forms.CharField(label="Nombre de la Empresa", max_length=100)
    email_admin = forms.EmailField(label="Correo del Administrador")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    confirmar_password = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")
        if password and password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data
