from django.urls import path
from usuarios import views as v

urlpatterns = [
    path('registro/', v.registro_usuario, name="registro"),
    path('login/', v.login_usuario, name="login"),
    path('logout/', v.logout_usuario, name="logout"),
    path('', v.index, name="index"),
    path('crear-arquitecto/', v.crear_arquitecto, name="crear-arquitecto"),
    path('quienes-somos/', v.quienes_somos, name='quienes-somos'),
    path('index-arquitecto/', v.index, name="index-arquitecto"),
    path('index-cliente/', v.index, name="index-cliente")
]
