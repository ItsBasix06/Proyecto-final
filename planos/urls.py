from django.urls import path
from . import views

urlpatterns = [
    # Rutas para el Index de Clientes
    path('mis-planos/', views.planos_clientes_ver, name='planos_clientes'),
    path('mis-planos/<int:id_plano>/', views.plano_cliente_info, name='plano_cliente_info'),
    path('solicitar-plano/', views.solicitar_plano_crear, name='solicitar_plano'),
    path('mis-planos/<int:id_plano>/eliminar/', views.eliminar_plano, name='eliminar_plano'),

    # Rutas para el Index de Arquitectos
    path('asignados/', views.planos_arquitectos_ver, name='planos_arquitectos'),
    path('asignados/<int:id_plano>/gestionar/', views.plano_arquitecto_info, name='plano_arquitecto_info'),
]