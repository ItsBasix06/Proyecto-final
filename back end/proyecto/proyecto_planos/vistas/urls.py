from django.urls import path
from . import views as vs

urlpatterns = [
    path('', vs.index, name="index"),
    path('login/', vs.login, name="login"),
    path('register/', vs.register, name="register"),
    path('recuperar/', vs.recuperar, name="recuperar"),
    path('quienes_somos/', vs.quienes_somos, name="quienes_somos"),
    path('index_admin/', vs.index_admin, name="index_admin"),
]