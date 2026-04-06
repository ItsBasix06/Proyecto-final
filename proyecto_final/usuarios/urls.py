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
    path('suscripciones/', vs.contratar_suscripcion, name="suscripciones"),
    path('suscripcion-exitosa/', vs.contratar_suscripcion, name="suscripcion-exitosa"),
    path('mi-arquitecto/', v.info_arquitecto, name='mi-arquitecto'),
]
