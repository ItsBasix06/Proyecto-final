from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Suscripcion
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
def contratar_suscripcion(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    suscripcion_existente = Suscripcion.objects.filter(cliente=cliente).first()

    if request.method == "POST":
        # --- CASO A: ELIMINAR ---
        if request.POST.get('accion') == 'eliminar':
            if suscripcion_existente:
                suscripcion_existente.delete()
                messages.success(request, "Suscripción eliminada correctamente.")
            return redirect('suscripciones')

        # --- CASO B: CONTRATAR O ACTUALIZAR ---
        tipo = request.POST.get('tipo_plan')
        precios = {'Basico': 9.99, 'Estandar': 19.99, 'Premium': 29.99}
        
        if tipo in precios:
            try:
                with transaction.atomic():
                    Suscripcion.objects.update_or_create(
                        cliente=cliente,
                        defaults={'tipo_suscripcion': tipo, 'precio': precios[tipo]}
                    )
                messages.success(request, f"¡Plan {tipo} activado con éxito!")
                # REDIRIGIMOS a la misma vista. 
                # Al volver a entrar por GET, se ejecutará la lógica de visualización de abajo.
                return redirect('suscripciones') 
            except Exception as e:
                messages.error(request, f"Hubo un problema al procesar tu suscripción: {e}")
                return redirect('suscripciones')

    # --- VISUALIZACIÓN (Manejo de GET) ---
    
    # Si ya tiene una suscripción y NO ha pulsado el botón de "Cambiar" (?cambiar=true)
    if suscripcion_existente and request.GET.get('cambiar') != 'true':
        return render(request, 'suscripciones/suscripcion_exitosa.html', {
            'suscripcion': suscripcion_existente
        })
    
    # Si es nuevo, o si quiere cambiar de plan (porque pulsó el botón "Actualizar")
    return render(request, 'suscripciones/suscripciones.html', {
        'cliente': cliente
    })