import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Plano

class SolicitarPlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['titulo', 'tamano', 'formato', 'archivo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Ej. Planta Baja Chalet Modular'
            }),
            'tamano': forms.NumberInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'Superficie en m²'
            }),
            'formato': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control rounded-3'
            }),
        }

    # Método para validar exclusivamente el campo "archivo"
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        
        if archivo:
            # Extraemos la extensión del archivo y la pasamos a minúsculas
            extension = os.path.splitext(archivo.name)[1].lower()
            # Definimos la lista de formatos permitidos
            extensiones_validas = ['.pdf', '.dwg', '.zip', '.rar']
            
            if extension not in extensiones_validas:
                raise ValidationError(
                    f"Formato no permitido ({extension}). Por favor, sube un archivo PDF, DWG o un comprimido ZIP/RAR."
                )
                
        return archivo
        
        
        