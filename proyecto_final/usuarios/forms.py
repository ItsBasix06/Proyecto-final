from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class RegistroArquitectoForm(UserCreationForm):
    nif = forms.CharField(max_length=9, min_length=9, label="NIF (DNI)")
    nombre = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=150)
    telefono = forms.CharField(max_length=9, min_length=9)
    email = forms.EmailField()

    # Validación personalizada para el Teléfono
    def clean_telefono(self):
        data = self.cleaned_data['telefono']
        if not data.isdigit():
            raise ValidationError("El teléfono solo puede contener números.")
        return data

    # Validación personalizada para el NIF
    def clean_nif(self):
        data = self.cleaned_data['nif'].upper()
        if not re.match(r'^[0-9]{8}[A-Z]$|^[A-Z][0-9]{8}$', data):
            raise ValidationError("El formato del NIF/CIF no es válido (8 números y 1 letra).")
        return data

class RegistroClienteForm(UserCreationForm):
    nif = forms.CharField(max_length=9, min_length=9)
    empresa = forms.CharField(max_length=200)
    telefono = forms.CharField(max_length=9, min_length=9)
    email = forms.EmailField()
    cuenta_bancaria = forms.CharField(max_length=24, min_length=24)

    def clean_telefono(self):
        data = self.cleaned_data['telefono']
        if not data.isdigit():
            raise ValidationError("El teléfono debe ser numérico.")
        return data

    def clean_cuenta_bancaria(self):
        # Limpiamos espacios por si el usuario pega el IBAN con ellos
        data = self.cleaned_data['cuenta_bancaria'].replace(" ", "").upper()
        if len(data) != 24:
            raise ValidationError("El IBAN debe tener 24 caracteres.")
        if not data.startswith('ES'):
            raise ValidationError("El IBAN debe comenzar por ES.")
        return data