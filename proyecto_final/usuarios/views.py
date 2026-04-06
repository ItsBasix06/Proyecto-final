from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from .models import Cliente, Arquitecto, MensajeContacto
from suscripciones.models import Suscripcion
from django.db import transaction
from .forms import RegistroArquitectoForm, RegistroClienteForm
from django.contrib.auth.decorators import login_required



# Decorador personalizado
def solo_grupo(nombre_grupo):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.groups.filter(name=nombre_grupo).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@solo_grupo('ARQUITECTO') # Solo los arquitectos pueden dar de alta clientes
def registro_cliente(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST) # Usamos el nuevo form con validaciones
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Creamos el usuario base (auth_user)
                    usuario_nuevo = form.save()

                    # 2. Creamos el perfil de Cliente con los datos limpios
                    # El form.cleaned_data ya tiene el IBAN sin espacios y el NIF en mayúsculas
                    Cliente.objects.create(
                        user=usuario_nuevo,
                        nif_cliente=form.cleaned_data['nif'],
                        nom_empresa=form.cleaned_data['empresa'],
                        telefono=form.cleaned_data['telefono'],
                        correo_electronico=form.cleaned_data['email'],
                        cuenta_bancaria=form.cleaned_data['cuenta_bancaria'],
                        # Vinculamos automáticamente al arquitecto que está logueado
                        arquitecto=request.user.perfil_arquitecto 
                    )

                    # 3. Asignamos el grupo CLIENTE
                    grupo, _ = Group.objects.get_or_create(name='CLIENTE')
                    usuario_nuevo.groups.add(grupo)

                messages.success(request, f"Cliente {form.cleaned_data['empresa']} registrado con éxito.")
                return redirect("index") # O a la lista de clientes si la tienes
                
            except Exception as e:
                # Si falla el NIF duplicado o cualquier cosa, transaction.atomic borra el usuario_nuevo
                messages.error(request, "Error: El NIF ya existe o los datos son incorrectos.")
    else:
        form = RegistroClienteForm()

    return render(request, "usuarios/crear_cliente.html", {"form": form})


def registro_arquitecto(request):
    if request.method == "POST":
        form = RegistroArquitectoForm(request.POST) # Usamos el nuevo form
        if form.is_valid():
            try:
                with transaction.atomic():
                    usuario = form.save()
                    # Los datos ya vienen "limpios" en form.cleaned_data
                    Arquitecto.objects.create(
                        user=usuario,
                        nif_arquitecto=form.cleaned_data['nif'],
                        nombre=form.cleaned_data['nombre'],
                        apellidos=form.cleaned_data['apellidos'],
                        telefono=form.cleaned_data['telefono'],
                        correo_electronico=form.cleaned_data['email']
                    )
                messages.success(request, "¡Registro completado!")
                return redirect("login")
            except Exception:
                messages.error(request, "Error al crear el perfil.")
    else:
        form = RegistroArquitectoForm()
    return render(request, "usuarios/registro_arquitecto.html", {"form": form})

def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f"Bienvenido, {usuario.username}")
            return redirect("index")
        else:
            # Si el formulario NO es válido, es que las credenciales fallaron
            messages.error(request, "Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
    else:
        form = AuthenticationForm()

    return render(request, "usuarios/login.html", {"form": form})

def logout_usuario(request):
    logout(request)
    messages.success(request, "Sesión cerrada.")
    return redirect("login")

def index(request):
    if request.user.is_authenticated:
        # CASO CLIENTE
        if hasattr(request.user, 'perfil_cliente'):
            cliente = request.user.perfil_cliente
            # Buscamos la suscripción vinculada a este cliente
            suscripcion = Suscripcion.objects.filter(cliente=cliente).first()
            
            return render(request, "usuarios/index_cliente.html", {
                'cliente': cliente,
                'suscripcion': suscripcion  # <--- Enviamos la suscripción al HTML
            })
        
        # CASO ARQUITECTO
        if hasattr(request.user, 'perfil_arquitecto'):
            return render(request, "usuarios/index_arquitecto.html", {
                'arquitecto': request.user.perfil_arquitecto
            })
     
    # Si no está autenticado
    return render(request, "usuarios/index.html")

def quienes_somos(request):
    return render(request, 'usuarios/quienes_somos.html')

@login_required
def info_arquitecto(request):
    # Obtenemos el perfil del cliente
    cliente = get_object_or_404(Cliente, user=request.user)
    
    # Obtenemos su arquitecto (ajusta 'arquitecto' según el nombre en tu modelo Cliente)
    arquitecto = cliente.arquitecto 

    if request.method == "POST":
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        # Lógica para guardar el mensaje
        MensajeContacto.objects.create(
            cliente=cliente,
            arquitecto=arquitecto,
            asunto=asunto,
            mensaje=mensaje
        )
        messages.success(request, "¡Mensaje enviado correctamente a tu arquitecto!")
        return redirect('tu_url_de_arquitecto') # Cambia por el name de tu URL

    return render(request, 'usuarios/arquitecto_info.html', {
        'arquitecto': arquitecto,
        'cliente': cliente
    })