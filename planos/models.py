from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Arquitecto, Cliente
from django.contrib.auth.models import User


class Plano(models.Model):
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('DWG', 'DWG'),
    ]

    ESTADO_CHOICES = [
        ('EN_PROCESO', 'En Proceso'),
        ('LISTO', 'Listo para Descarga'),
    ]

    id_plano = models.AutoField(primary_key=True, verbose_name="ID Plano")
    
    titulo = models.CharField(
        max_length=150, 
        verbose_name="Título / Descripción del Plano",
        help_text="Ej: Plano Eléctrico Cocina o Distribución Planta Baja"
    )
    
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='planos_solicitados',
        verbose_name="Cliente Solicitante"
    )
    
    # Utilizo RESTRICT para no perder información valiosa como los planos calculados. 
    # Para eliminar un arquitecto tendria q eliminar sus planos o mejor reasignarlos a otro para no perder los planos
    arquitecto = models.ForeignKey(
        Arquitecto, 
        on_delete=models.RESTRICT, 
        related_name='planos_asignados',
        verbose_name="Arquitecto Diseñador"
    ) 
    
    tamano = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        blank=False,
        default=0.01,
        verbose_name="Tamaño (m²)"
    )
    
    formato = models.CharField(
        max_length=50,
        choices=FORMATO_CHOICES,
        blank=False,
        default='PDF',
        verbose_name="Formato"
    )
    
    # Archivo inicial (croquis, boceto o instrucciones)
    archivo = models.FileField(
        upload_to='planos_clientes/', 
        blank=True, 
        null=True, 
        verbose_name="Archivo Base del Cliente"
    )
    
    # Archivo técnico definitivo ya calculado y corregido
    archivo_procesado = models.FileField(
        upload_to='planos_procesados/', 
        blank=True, 
        null=True, 
        verbose_name="Archivo Procesado (Arquitecto)"
    )
    
    # Estado del Plano (Para la tabla del Cliente y el Arquitecto)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='EN_PROCESO',
        verbose_name="Estado del Trabajo"
    )
    
    fecha_subida = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Subida"
    )
    
    fecha_entrega = models.DateField(
        blank=False, 
        default='2026-01-01', 
        verbose_name="Fecha de Entrega"
    )

    def __str__(self):
        return f"Plano #{self.id_plano} - {self.titulo} ({self.cliente.nom_empresa})"