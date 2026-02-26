from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente
from django.contrib.auth import login, logout

def registro_usuario(request):
    """
    Registro de usuarios CLIENTE.
    El arquitecto NO se registra por aquí.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            # Se crea automáticamente el perfil Cliente
            Cliente.objects.create(user=usuario)

            messages.success(request, "Cliente registrado con éxito")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "usuarios/registro.html", {"form": form})


def login_usuario(request):
    """
    Login único para clientes y arquitectos.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, "Has iniciado sesión correctamente")
            return redirect("inicio")
    else:
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})

def logout_usuario(request):
    """
    Cierre de sesión del usuario.
    """
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente")
    return redirect("login")

def inicio(request):
    if request.user.is_authenticated:
        mensaje = f"Hola, {request.user.username}"
    else:
        mensaje = "No has iniciado sesión"

    return render(request, "usuarios/inicio.html", {"mensaje": mensaje})

