from django.contrib import admin
from django.utils.html import format_html
from .models import Plano

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    # 1. Columnas de la tabla principal
    # 'link_archivo' es una función que creamos abajo para descargar el archivo
    list_display = (
        'id_plano', 
        'arquitecto', 
        'formato', 
        'tamano', 
        'fecha_subida', 
        'fecha_entrega', 
        'link_archivo'
    )

    # 2. Filtros laterales
    # Permite filtrar por arquitecto, formato de archivo y fechas
    list_filter = ('arquitecto', 'formato', 'fecha_subida')

    # 3. Buscador
    # Busca por ID de plano o por nombre/apellido del arquitecto relacionado
    search_fields = ('id_plano', 'arquitecto__nombre', 'arquitecto__apellidos')

    # 4. Campo de solo lectura para la fecha de subida (ya que es auto_now_add)
    readonly_fields = ('fecha_subida',)

    # 5. Función para mostrar un botón de "Descargar" en la lista
    def link_archivo(self, obj):
        if obj.archivo:
            return format_html('<a href="{}" target="_blank">📄 Descargar</a>', obj.archivo.url)
        return "Sin archivo"
    
    link_archivo.short_description = 'Archivo'