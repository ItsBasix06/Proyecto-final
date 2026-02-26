from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cliente {self.user.username}"
    

class Arquitecto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clientes = models.ManyToManyField(
        Cliente,
        related_name='arquitectos'
    )

    def __str__(self):
        return f"Arquitecto {self.user.username}"