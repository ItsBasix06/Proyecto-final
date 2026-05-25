import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plano
from usuarios.models import Arquitecto, Cliente
from .forms import SolicitarPlanoForm

# =========================================================================
# INDEX DE CLIENTES
# =========================================================================

@login_required
def planos_clientes_ver(request):
    """
    Muestra la tabla con todos los planos del cliente logueado.
    """
    # Intentamos obtener el perfil de Cliente del usuario actual
    try:
        perfil_cliente = request.user.perfil_cliente
    except Cliente.DoesNotExist:
        messages.error(request, "No tienes un perfil de cliente asociado.")
        return redirect('inicio') # O la página que maneje el error

    # Recuperamos todos los planos de este cliente específico
    planos = Plano.objects.filter(cliente=perfil_cliente).order_by('-fecha_subida')
    
    context = {
        'planos': planos
    }
    return render(request, 'planos/planos_clientes.html', context)


@login_required
def plano_cliente_info(request, id_plano):
    """
    Detalle del plano para el cliente.
    Maneja la subida del archivo base, su validación de formato,
    la eliminación de la solicitud y el control real de suscripción para descargas.
    """
    # Obtenemos el perfil del cliente logueado
    perfil_cliente = get_object_or_404(Cliente, user=request.user)
    # Buscamos el plano asegurando que pertenezca a este cliente concreto
    plano = get_object_or_404(Plano, id_plano=id_plano, cliente=perfil_cliente)
    
    # --- LÓGICA DE NEGOCIO REAL: Control de suscripción ---
    # REVISIÓN: Cambia 'tiene_suscripcion_activa' por el nombre exacto del campo de tu modelo Cliente
    if perfil_cliente.tiene_suscripcion_activa:
        permitir_descarga = True
    else:
        permitir_descarga = False

    # --- Manejo del Formulario de la Columna Izquierda (Subida/Actualización de archivo) ---
    if request.method == 'POST' and 'subir_base' in request.POST:
        nuevo_archivo = request.FILES.get('archivo_base')
        if nuevo_archivo:
            # 1. Extraemos la extensión del archivo y la pasamos a minúsculas
            extension = os.path.splitext(nuevo_archivo.name)[1].lower()
            extensiones_validas = ['.pdf', '.dwg', '.zip', '.rar']
            
            # 2. VALIDACIÓN DE FORMATO: Bloqueamos extensiones como .png
            if extension not in extensiones_validas:
                messages.error(
                    request, 
                    f"Error: El formato {extension} no está permitido. Solo se admiten archivos .pdf, .dwg o comprimidos ZIP/RAR."
                )
                return redirect('plano_cliente_info', id_plano=plano.id_plano)
            
            # 3. Guardado seguro si supera el filtro
            plano.archivo = nuevo_archivo
            plano.estado = 'EN_PROCESO'  # Cambia el estado automáticamente si decide resubirlo
            plano.save()
            messages.success(request, "Archivo base enviado al arquitecto correctamente.")
            return redirect('plano_cliente_info', id_plano=plano.id_plano)

    # Preparación del contexto para la plantilla HTML
    context = {
        'plano': plano,
        'permitir_descarga': permitir_descarga
    }
    return render(request, 'planos/plano_cliente_info.html', context)


# =========================================================================
# INDEX DE ARQUITECTOS
# =========================================================================

@login_required
def planos_arquitectos_ver(request):
    """
    Muestra la tabla de todos los planos asignados al arquitecto logueado.
    """
    # Dependiendo de cómo vincules al Arquitecto con el User de Django:
    # Si tu modelo Arquitecto tiene una relación con User (ej: perfil_arquitecto)
    try:
        perfil_arquitecto = request.user.perfil_arquitecto
    except AttributeError:
        # Si el usuario es directamente el arquitecto o manejas otra relación, adáptalo
        perfil_arquitecto = get_object_or_404(Arquitecto, user=request.user)

    # Filtramos los planos asignados a este arquitecto
    planos = Plano.objects.filter(arquitecto=perfil_arquitecto).order_by('-fecha_subida')
    
    context = {
        'planos': planos
    }
    return render(request, 'planos/planos_arquitectos.html', context)


@login_required
def plano_arquitecto_info(request, id_plano):
    """
    Detalle del plano para el arquitecto (Doble columna).
    Permite descargar el archivo base del cliente y subir el cálculo procesado.
    """
    # Obtenemos el arquitecto logueado (adapta la obtención según tu modelo)
    try:
        perfil_arquitecto = request.user.perfil_arquitecto
    except AttributeError:
        perfil_arquitecto = get_object_or_404(Arquitecto, user=request.user)
        
    # Conseguimos el plano garantizando que pertenece a este arquitecto
    plano = get_object_or_404(Plano, id_plano=id_plano, arquitecto=perfil_arquitecto)

    # --- Manejo del Formulario de la Columna Derecha (Subida de plano procesado) ---
    if request.method == 'POST' and 'subir_calculo' in request.POST:
        archivo_final = request.FILES.get('archivo_tecnico')
        if archivo_final:
            plano.archivo_procesado = archivo_final
            plano.estado = 'LISTO' # Cambiamos el estado automáticamente a listo para descarga
            plano.save()
            messages.success(request, "Entrega final procesada y guardada en el sistema.")
            return redirect('plano_arquitecto_info', id_plano=plano.id_plano)

    context = {
        'plano': plano
    }
    return render(request, 'planos/plano_arquitecto_info.html', context)


@login_required
def solicitar_plano_crear(request):
    # Comprobamos que el usuario logueado sea un cliente real
    try:
        perfil_cliente = request.user.perfil_cliente
    except AttributeError:
        messages.error(request, "Acceso denegado. Solo los perfiles de clientes pueden solicitar planos.")
        return redirect('index')

    if request.method == 'POST':
        form = SolicitarPlanoForm(request.POST, request.FILES)
        if form.is_valid():
            # Creamos el objeto plano sin guardarlo en la Base de Datos todavía
            nuevo_plano = form.save(commit=False)
            
            # Automatización de campos de auditoría:
            nuevo_plano.cliente = perfil_cliente
            # Le asignamos automáticamente el arquitecto que tiene este cliente asignado
            nuevo_plano.arquitecto = perfil_cliente.arquitecto
            nuevo_plano.estado = 'EN_PROCESO' # Nace en proceso de cálculo
            
            # Guardamos definitivamente
            nuevo_plano.save()
            
            messages.success(request, f"¡Solicitud del plano '{nuevo_plano.titulo}' creada con éxito!")
            return redirect('planos_clientes')
    else:
        form = SolicitarPlanoForm()
        
    return render(request, 'planos/solicitar_plano.html', {'form': form})

@login_required
def eliminar_plano(request, id_plano):
    # Aseguramos que el cliente solo pueda buscar entre SUS propios planos
    perfil_cliente = get_object_or_404(Cliente, user=request.user)
    plano = get_object_or_404(Plano, id_plano=id_plano, cliente=perfil_cliente)
    
    # CONTROL DE SEGURIDAD: Solo borrar si no está finalizado
    if plano.estado == 'FINALIZADO':
        messages.error(request, "No puedes eliminar un plano que ya ha sido finalizado por el arquitecto.")
        return redirect('plano_cliente_info', id_plano=plano.id_plano)
        
    if request.method == 'POST':
        titulo_eliminado = plano.titulo
        plano.delete()
        messages.success(request, f"La solicitud del plano '{titulo_eliminado}' ha sido eliminada correctamente.")
        return redirect('planos_clientes') # Redirige a la tabla general de planos
        
    # Si por algún motivo entran por GET, redirigimos al detalle
    return redirect('plano_cliente_info', id_plano=plano.id_plano)