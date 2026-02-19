from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 

from django.shortcuts import render

def index(request):
    return render(request, "vistas/index.html")

def login(request):
    """
    Vista de inicio de sesión.
    - GET: muestra el formulario de login
    - POST: valida credenciales y crea la sesión
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Obtener credenciales validadas
            usuario = form.get_user()
            # Crear sesión de usuario
            login(request, usuario)
            return redirect("index")
    else:
        form = AuthenticationForm()

    return render(request, "vistas/login.html", {"form": form})

def register(request):
    """
    Vista de registro de usuarios.
    - GET: muestra el formulario de registro
    - POST: valida credenciales, crea el usuario y inicia sesión automaticamente
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Crear usuario
            usuario = form.save()
            # Iniciar sesión automáticamente
            login(request, usuario)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "vistas/register.html", {"form": form})

@login_required
def logout(request):
    """
    Vista de cierre de sesión.
    Elimina la sesión del usuario actual.
    """
    logout(request)
    return redirect("login")

def recuperar(request):
    return render(request, "vistas/recuperar-password.html")

def quienes_somos(request):
    return render(request, "vistas/quienes-somos.html")

def index_admin(request):
    return render(request, "vistas/index-admin.html")