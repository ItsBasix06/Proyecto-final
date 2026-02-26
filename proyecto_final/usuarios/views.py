from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 

def registro_usuario(request):
    """
    Vista de registro de usuarios.
    - GET: muestra el formulario de registro.
    - POST: valida credenciales, crea el usuario y redirige al login.
    """
    if request.method == "POST":
        # Se procesa el formulario con los datos enviados
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Se guarda el nuevo usuario en la base de datos
            usuario = form.save()
            messages.success(request, "Usuario registrado con éxito")
            return redirect("login")
    else:
        # Se envía un formulario de registro vacío
        form = UserCreationForm()

    return render(request, "usuarios/registro.html", {"form": form})


def login_usuario(request):
    """
    Vista de inicio de sesión.
    - GET: muestra el formulario de login.
    - POST: valida credenciales y crea la sesión del usuario.
    """
    if request.method == "POST":
        # AuthenticationForm requiere el objeto request y los datos POST
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Se extrae el usuario validado del formulario
            usuario = form.get_user()
            # Se crea la sesión en el navegador
            login(request, usuario)
            messages.success(request, "Has iniciado sesión correctamente")
            return redirect("inicio")
    else:
        # Formulario de login vacío
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})


def logout_usuario(request):
    """
    Vista de cierre de sesión.
    Elimina la sesión del usuario actual y redirige al login.
    """
    # Elimina los datos de sesión del usuario
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente")
    return redirect("login")


def inicio(request):
    """
    Vista de la página principal.
    Muestra un mensaje de bienvenida personalizado y la lista total de productos.
    """
    # Lógica para personalizar el saludo según el estado de la sesión
    if request.user.is_authenticated:
        mensaje = f"Hola, {request.user.username}"
    else:
        mensaje = "No has iniciado sesión"

    return render(request, "usuarios/inicio.html", {"mensaje": mensaje})