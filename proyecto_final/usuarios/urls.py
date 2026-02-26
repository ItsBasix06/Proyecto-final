from django.urls import path
from usuarios import views as v

urlpatterns = [
    path('registro/', v.registro_usuario, name="registro"),
    path('login/', v.login_usuario, name="login"),
    path('logout/', v.logout_usuario, name="logout"),
    path('', v.inicio, name="inicio"),
]
