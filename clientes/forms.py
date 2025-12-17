from django import forms
from .models import Cliente
from django.core.exceptions import ValidationError

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Este correo ya está en uso.")
        return email
