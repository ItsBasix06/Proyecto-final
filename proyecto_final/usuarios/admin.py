from django.contrib import admin
from .models import Cliente, Arquitecto

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')

@admin.register(Arquitecto)
class ArquitectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('clientes',)