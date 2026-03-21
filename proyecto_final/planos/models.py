from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import CheckConstraint, Q

class Suscripcion(models.Model):
    """
    Modelo que representa una suscripción en el sistema.

    Este modelo se basa en la estructura SQL proporcionada, adaptada a Django.
    - El campo 'id_suscripcion' es el equivalente al Id_Suscripcion en SQL, actuando como clave primaria auto-incremental.
    - 'tipo_suscripcion' almacena el tipo de suscripción, restringido a valores específicos mediante 'choices'.
    - 'precio' almacena el precio de la suscripción, con validación para asegurar que sea mayor que 0.
    - 'nif_cliente' es una clave foránea que referencia al campo 'nif' del modelo Cliente, con restricción en borrado.

    Constraints adicionales:
    - Check para asegurar que el precio sea mayor que 0 (usando CheckConstraint en Meta).
    - Los tipos de suscripción están limitados a 'Basico', 'Premium', 'Enterprise' o 'Custom' mediante choices y una constraint implícita.

    Notas:
    - Se asume que existe un modelo 'Cliente' con un campo 'nif' único (puede ser primary_key o unique=True).
    - En Django, el nombre de la tabla por defecto sería 'nombre_app_suscripcion' (minusculas), pero puedes
      configurar 'db_table = "Suscripciones"' en la clase Meta si necesitas coincidir exactamente con el nombre SQL.
    - Para usar este modelo, asegúrate de que 'Cliente' esté definido en el mismo módulo o importado correctamente.
    """

    TIPO_CHOICES = [
        ('Basico', 'Básico'),
        ('Premium', 'Premium'),
        ('Enterprise', 'Enterprise'),
        ('Custom', 'Custom'),
    ]

    id_suscripcion = models.AutoField(
        primary_key=True,
        verbose_name="ID de Suscripción"
    )
    """Campo auto-incremental que actúa como clave primaria."""

    tipo_suscripcion = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        null=False,
        blank=False,
        verbose_name="Tipo de Suscripción"
    )
    """Tipo de suscripción, limitado a opciones predefinidas."""

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(0.01)],  # Valida en el nivel de formulario/modelo que sea > 0
        verbose_name="Precio"
    )
    """Precio de la suscripción, debe ser mayor que 0."""

    nif_cliente = models.ForeignKey(
        'Cliente',  # Asume que el modelo Cliente existe
        on_delete=models.RESTRICT,
        to_field='nif',  # Referencia al campo 'nif' en Cliente
        null=False,
        blank=False,
        verbose_name="NIF del Cliente"
    )
    """Clave foránea al NIF del cliente, con restricción en borrado."""

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"
        constraints = [
            CheckConstraint(
                check=Q(precio__gt=0),
                name='chk_precio'
            ),
            # La restricción de tipos se maneja con choices, pero si se necesita una constraint en BD:
            CheckConstraint(
                check=Q(tipo_suscripcion__in=['Basico', 'Premium', 'Enterprise', 'Custom']),
                name='chk_tipo_suscripcion'
            ),
        ]
        # Si necesitas forzar el nombre de la tabla en la BD:
        # db_table = 'Suscripciones'