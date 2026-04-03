from django.contrib import admin
from .models import Suscripcion

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    # 1. Columnas que verás en la tabla principal
    list_display = (
        'id_suscripcion', 
        'tipo_suscripcion', 
        'cliente', 
        'precio_formateado' # Usamos una función para añadir el símbolo €
    )

    # 2. Filtros laterales (muy útil cuando tengas cientos de suscripciones)
    list_filter = ('tipo_suscripcion',)

    # 3. Buscador: Permite buscar por el nombre de la empresa del cliente
    # Nota: Usamos cliente__nom_empresa para acceder al campo del modelo Cliente
    search_fields = ('cliente__nom_empresa', 'tipo_suscripcion')

    # 4. Edición rápida: Permite cambiar el precio desde la lista sin entrar al detalle
    list_editable = ('tipo_suscripcion',)

    # 5. Mejora visual para el precio
    def precio_formateado(self, obj):
        return f"{obj.precio} €"
    precio_formateado.short_description = 'Precio'