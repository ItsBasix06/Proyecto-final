from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from .models import Cliente, Arquitecto, MensajeContacto
from suscripciones.models import Suscripcion
from django.db import transaction
from .forms import RegistroArquitectoForm, RegistroClienteForm, ClienteEditarForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from planos.models import Plano


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

@login_required
def eliminar_cliente(request, user_id):
    """
    Elimina un cliente y su usuario de forma limpia sin romper las 
    referencias en memoria de Django.
    """
    if Cliente.objects.filter(user=request.user).exists():
        messages.error(request, "No tienes permisos para realizar esta acción.")
        return redirect('planos_clientes')

    if request.method == "POST":
        # 1. Buscamos el cliente usando el user_id de la URL
        cliente = get_object_or_404(Cliente, user__id=user_id)
        usuario = cliente.user 
        
        # 2. Guardamos el nombre en una variable de texto simple (así no depende de la BD)
        nombre_cliente = usuario.get_full_name() or usuario.username
        
        # 3. Borramos primero el Cliente. Si la cascada está al revés, esto evitará el error.
        # Para asegurar que ambos se borren sin lanzar el 'DoesNotExist', los eliminamos al mismo tiempo:
        cliente.delete()
        if usuario and usuario.id:
            usuario.delete()
        
        # 4. Mostramos el mensaje con la variable de texto limpia
        messages.success(request, f"El cliente {nombre_cliente} ha sido eliminado correctamente.")
    
    return redirect('lista_clientes')

@login_required
def editar_cliente(request, user_id):
    """Vista simplificada para editar los datos comerciales de la ficha del cliente."""
    # Control de seguridad para que los clientes no entren aquí
    if Cliente.objects.filter(user=request.user).exists():
        return redirect('planos_clientes')

    # Buscamos al cliente por el ID de su usuario (ocultando el NIF de la URL)
    cliente = get_object_or_404(Cliente, user__id=user_id)

    if request.method == 'POST':
        # Pasamos los datos del formulario de edición
        form = ClienteEditarForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f"Los datos de {cliente.nom_empresa} se han actualizado correctamente.")
            return redirect('lista_clientes')
    else:
        # Si entran por primera vez, precargamos los datos actuales
        form = ClienteEditarForm(instance=cliente)

    context = {
        'cliente_form': form,
        'cliente': cliente
    }
    return render(request, 'usuarios/cliente_edit.html', context)

@login_required
def lista_clientes(request):
    """
    Vista para el panel del Arquitecto.
    Usa 'planos_solicitados' que es el nombre correcto detectado en los campos de Cliente.
    """
    # CONTROL DE SEGURIDAD:
    if Cliente.objects.filter(user=request.user).exists():
        messages.error(request, "No tienes permisos de arquitecto para acceder a esta sección.")
        return redirect('planos_clientes')

    # ¡EL CAMBIO ESTÁ AQUÍ!: Cambiamos Count('plano') por Count('planos_solicitados')
    clientes = Cliente.objects.annotate(total_planos=Count('planos_solicitados')).order_by('user__first_name')

    context = {
        'clientes': clientes
    }
    
    return render(request, 'usuarios/clientes.html', context)


@login_required
def detalle_cliente(request, user_id):
    """
    Muestra la ficha del cliente buscando de forma segura por el ID de su Usuario,
    evitando exponer el NIF/DNI en la URL de la web.
    """
    if Cliente.objects.filter(user=request.user).exists():
        return redirect('planos_clientes')

    # Buscamos al cliente filtrando por la ID de su relación 'user'
    cliente = get_object_or_404(Cliente, user__id=user_id)
    
    # El resto de la lógica se queda exactamente igual
    planos = Plano.objects.filter(cliente=cliente).order_by('-id_plano')

    context = {
        'cliente': cliente,
        'planos': planos,
    }
    return render(request, 'usuarios/cliente_detail.html', context)


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

                    # 3. Asignamos el grupo ARQUITECTO
                    grupo, _ = Group.objects.get_or_create(name='ARQUITECTO')
                    usuario.groups.add(grupo)

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

