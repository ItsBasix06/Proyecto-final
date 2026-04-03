from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Suscripcion
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
def contratar_suscripcion(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    suscripcion_existente = Suscripcion.objects.filter(cliente=cliente).first()

    # --- ACCIÓN: ELIMINAR ---
    if request.method == "POST" and request.POST.get('accion') == 'eliminar':
        if suscripcion_existente:
            suscripcion_existente.delete()
            messages.success(request, "Suscripción eliminada correctamente.")
        return redirect('suscripciones')

    # --- ACCIÓN: CREAR O ACTUALIZAR ---
    if request.method == "POST":
        tipo = request.POST.get('tipo_plan')
        precios = {'Basico': 9.99, 'Estandar': 19.99, 'Premium': 29.99}
        
        if tipo in precios:
            try:
                with transaction.atomic():
                    suscripcion, creado = Suscripcion.objects.update_or_create(
                        cliente=cliente,
                        defaults={'tipo_suscripcion': tipo, 'precio': precios[tipo]}
                    )
                    return render(request, 'suscripciones/suscripcion_exitosa.html', {'suscripcion': suscripcion})
            except Exception as e:
                messages.error(request, f"Error: {e}")

    # --- VISUALIZACIÓN ---
    # Si ya está suscrito y NO viene de darle al botón "Cambiar"
    if suscripcion_existente and request.GET.get('cambiar') != 'true':
        return render(request, 'suscripciones/suscripcion_exitosa.html', {'suscripcion': suscripcion_existente})
    
    # En cualquier otro caso (nuevo o quiere cambiar), mostramos planes
    return render(request, 'suscripciones/suscripciones.html', {'cliente': cliente})