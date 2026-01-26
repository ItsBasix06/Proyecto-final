from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
import datetime

def index(request):
    return render(request,"vistas/index.html")