from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
import datetime

from django.shortcuts import render

def index(request):
    return render(request, "vistas/index.html")

def login(request):
    return render(request, "vistas/login.html")

def register(request):
    return render(request, "vistas/register.html")

def recuperar(request):
    return render(request, "vistas/recuperar-password.html")

def quienes_somos(request):
    return render(request, "vistas/quienes-somos.html")

def index_admin(request):
    return render(request, "vistas/index-admin.html")