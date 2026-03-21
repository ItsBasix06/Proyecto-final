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
        verbose_name="Tamaño (m²)"
    )
    formato = models.CharField(
        max_length=50,
        choices=FORMATO_CHOICES,
        blank=False,
        verbose_name="Formato"
    )
    fecha_subida = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Subida"
    )
    fecha_entrega = models.DateField(blank=False, verbose_name="Fecha de Entrega")
    dni_usuario = models.ForeignKey(
        'usuarios.Arquitecto',
        on_delete=models.RESTRICT,
        blank=False,
        verbose_name="Arquitecto Diseñador"
    ) 


