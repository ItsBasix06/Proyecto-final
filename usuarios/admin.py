from django.contrib import admin
from .models import Arquitecto, Cliente

@admin.register(Arquitecto)
class ArquitectoAdmin(admin.ModelAdmin):
    # Añadimos 'user' para ver qué cuenta de sistema tiene asociada
    list_display = ('nif_arquitecto', 'user', 'nombre', 'apellidos', 'telefono', 'correo_electronico')
    
    # Podemos buscar también por el nombre de usuario de Django
    search_fields = ('nif_arquitecto', 'nombre', 'apellidos', 'user__username')
    
    ordering = ('apellidos',)
    
    # Agrupamos el campo User al principio en el formulario de edición
    fields = ('user', 'nif_arquitecto', 'nombre', 'apellidos', 'telefono', 'correo_electronico')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Añadimos 'user' a la lista
    list_display = ('nif_cliente', 'user', 'nom_empresa', 'telefono', 'arquitecto')
    
    list_filter = ('arquitecto',)
    
    # Búsqueda extendida al username
    search_fields = ('nif_cliente', 'nom_empresa', 'user__username')
    
    raw_id_fields = ('arquitecto', 'user') # 'user' también como raw_id por si hay cientos de usuarios
    
    fields = ('user', 'nif_cliente', 'nom_empresa', 'telefono', 'correo_electronico', 'cuenta_bancaria', 'arquitecto')