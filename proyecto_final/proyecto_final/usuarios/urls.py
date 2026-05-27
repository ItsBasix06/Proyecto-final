from django.urls import path
from usuarios import views as v
from suscripciones import views as vs

urlpatterns = [
    path('registro-cliente/', v.registro_cliente, name="registro-cliente"),
    path('login/', v.login_usuario, name="login"),
    path('logout/', v.logout_usuario, name="logout"),
    path('', v.index, name="index"),
    path('registro-arquitecto/', v.registro_arquitecto, name="registro-arquitecto"),
    path('quienes-somos/', v.quienes_somos, name='quienes-somos'),
    path('servicios/', v.servicios, name='servicios'),
    path('suscripciones/', vs.contratar_suscripcion, name="suscripciones"),
    path('suscripcion-exitosa/', vs.contratar_suscripcion, name="suscripcion-exitosa"),
    path('clientes/', v.lista_clientes, name='lista_clientes'),
    path('clientes/eliminar/<int:user_id>/', v.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/<int:user_id>/', v.detalle_cliente, name='detalle_cliente'),
    path('clientes/editar/<int:user_id>/', v.editar_cliente, name='editar_cliente'),
]
