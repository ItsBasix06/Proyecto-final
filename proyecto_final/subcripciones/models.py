from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Cliente

# Create your models here.
class Suscripcion(models.Model):
    TIPO_CHOICES = [
        ('Basico', 'Básico'),
        ('Premium', 'Premium'),
        ('Estándar', 'Estándar'),
    ]

    id_suscripcion = models.AutoField(primary_key=True, verbose_name="ID Suscripción")
    tipo_suscripcion = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        blank=False,
        verbose_name="Tipo de Suscripción"
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=False,
        verbose_name="Precio"
    )
    nif_cliente = models.ForeignKey(
        'usuarios.Cliente',
        on_delete=models.RESTRICT,
        verbose_name="Cliente"
    )
