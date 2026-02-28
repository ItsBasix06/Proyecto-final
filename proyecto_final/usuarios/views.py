from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from .models import Arquitecto

def solo_grupo(nombre_grupo):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if not request.user.groups.filter(name=nombre_grupo).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def registro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            # Crear perfil cliente
            Cliente.objects.create(user=usuario)

            # Asignar grupo CLIENTE
            grupo_cliente = Group.objects.get(name='CLIENTE')
            usuario.groups.add(grupo_cliente)

            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "usuarios/registro.html", {"form": form})

@solo_grupo('CLIENTE')
def crear_arquitecto(request):
    # Solo CLIENTES pueden crear arquitectos
    if not request.user.groups.filter(name='CLIENTE').exists():
        raise PermissionDenied

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Arquitecto.objects.create(user=user)

        # Asignar grupo ARQUITECTO
        grupo_arquitecto = Group.objects.get(name='ARQUITECTO')
        user.groups.add(grupo_arquitecto)

        return redirect("index")

    return render(request, "usuarios/crear_arquitecto.html")

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
            return redirect("index")
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

def quienes_somos(request):
    # Esta vista simplemente renderiza el template que creamos antes
    return render(request, 'usuarios/quienes_somos.html')

def index(request):
    if request.user.is_authenticated:
        mensaje = f"Hola, {request.user.username}"
    else:
        mensaje = "No has iniciado sesión"

    return render(request, "usuarios/index.html", {"mensaje": mensaje})

