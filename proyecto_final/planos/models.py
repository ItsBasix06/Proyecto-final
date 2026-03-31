from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Arquitecto

class Plano(models.Model):
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('DWG', 'DWG'),
    ]

    id_plano = models.AutoField(primary_key=True, verbose_name="ID Plano")
    
    tamano = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=False,
        default=0.01,  # Valor por defecto para registros antiguos
        verbose_name="Tamaño (m²)"
    )
    
    formato = models.CharField(
        max_length=50,
        choices=FORMATO_CHOICES,
        blank=False,
        default='PDF',  # Valor por defecto
        verbose_name="Formato"
    )
    
    archivo = models.FileField(
        upload_to='planos_archivos/', 
        blank=False, 
        null=True, # Al ser null=True, Django no te pedirá default para este
        verbose_name="Archivo del Plano"
    )
    
    fecha_subida = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Subida"
    )
    
    # Para fechas, puedes usar una cadena fija o importar 'timezone'
    fecha_entrega = models.DateField(
        blank=False, 
        default='2024-01-01', # Fecha genérica para salir del paso
        verbose_name="Fecha de Entrega"
    )
    
    arquitecto = models.ForeignKey(
        Arquitecto, 
        on_delete=models.RESTRICT, # models.RESTRICT significa que Django no te permitirá borrar a un Arquitecto si este tiene Clientes o Planos asociados.
        blank=False,
        # OJO: Si usas default aquí, debe ser un ID de un Arquitecto que ya exista.
        # Es mejor dejar este campo sin default y que Django te lo pida UNA vez 
        # o poner null=True temporalmente si no quieres complicaciones.
        verbose_name="Arquitecto Diseñador"
    ) 

    def __str__(self):
        return f"Plano {self.id_plano} - {self.formato}"