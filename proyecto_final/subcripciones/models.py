from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Cliente

# Create your models here.
class Suscripcion(models.Model):
    TIPO_CHOICES = [
        ('Basico', 'Básico'),
        ('Premium', 'Premium'),
        ('Estandar', 'Estándar'),
    ]

    id_suscripcion = models.AutoField(primary_key=True, verbose_name="ID Suscripción")
    
    tipo_suscripcion = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        blank=False,
        default='Basico',  # Valor por defecto para registros antiguos
        verbose_name="Tipo de Suscripción"
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=False,
        default=9.99,  # Un precio base por defecto
        verbose_name="Precio"
    )

    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.RESTRICT,
        verbose_name="Cliente",
    )

    def __str__(self):
        return f"Suscripción {self.tipo_suscripcion} - {self.cliente}"