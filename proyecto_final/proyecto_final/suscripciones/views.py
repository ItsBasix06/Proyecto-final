from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from .models import Suscripcion 
from usuarios.models import Cliente 

def contratar_suscripcion(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    suscripcion_existente = Suscripcion.objects.filter(cliente=cliente).first()

    if request.method == "POST":
        # --- CASO A: ELIMINAR ---
        if request.POST.get('accion') == 'eliminar':
            if suscripcion_existente:
                with transaction.atomic():
                    suscripcion_existente.delete()
                    # Al eliminar el plan, bloqueamos las descargas
                    cliente.tiene_suscripcion_activa = False
                    cliente.save()
                
                messages.success(request, "Suscripción eliminada correctamente. Tus descargas han sido bloqueadas.")
            return redirect('suscripciones')

        # --- CASO B: CONTRATAR O ACTUALIZAR ---
        tipo = request.POST.get('tipo_plan')
        precios = {'Basico': 9.99, 'Estandar': 19.99, 'Premium': 29.99}
        
        if tipo in precios:
            try:
                with transaction.atomic():
                    # 1. Creamos o actualizamos el registro de la suscripción
                    Suscripcion.objects.update_or_create(
                        cliente=cliente,
                        defaults={'tipo_suscripcion': tipo, 'precio': precios[tipo]}
                    )
                    # 2.  Activamos la casilla del cliente en la BD
                    cliente.tiene_suscripcion_activa = True
                    cliente.save()
                    
                messages.success(request, f"¡Plan {tipo} activado con éxito! Tus descargas ya están disponibles.")
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
