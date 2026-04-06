from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Arquitecto(models.Model):
    # Relación con el sistema de autenticación de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_arquitecto', null=True, blank=True)
    
    nif_arquitecto = models.CharField(max_length=20, primary_key=True, verbose_name="NIF") 
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(unique=True)

    def __str__(self):
        return f"Arquitecto: {self.nombre} {self.apellidos} ({self.user.username if self.user else 'Sin User'})"

class Cliente(models.Model):
    # Relación con el sistema de autenticación de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente', null=True, blank=True)
    
    nif_cliente = models.CharField(max_length=20, primary_key=True, verbose_name="NIF")
    nom_empresa = models.CharField(max_length=200, verbose_name="Nombre de la Empresa")
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(unique=True)
    cuenta_bancaria = models.CharField(max_length=50)
    
    arquitecto = models.ForeignKey(
        Arquitecto, 
        on_delete=models.CASCADE, 
        related_name='clientes',
        verbose_name="Arquitecto Diseñador"
    )

    def __str__(self):
        return f"Cliente: {self.nom_empresa} ({self.user.username if self.user else 'Sin User'})"
    
# En alguna de tus apps (ej. usuarios/models.py)
class MensajeContacto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    arquitecto = models.ForeignKey(Arquitecto, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

# Cuando se elimine un Arquitecto, borra su User asociado
@receiver(post_delete, sender=Arquitecto)
def eliminar_user_arquitecto(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

# Cuando se elimine un Cliente, borra su User asociado
@receiver(post_delete, sender=Cliente)
def eliminar_user_cliente(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()