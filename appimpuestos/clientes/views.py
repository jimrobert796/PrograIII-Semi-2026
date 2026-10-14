from django.shortcuts import render
from django.http import HttpResponse # Libreria de uso respuesta http

# Create your views here.
def holaMundo(request):
    return HttpResponse("Hola Mundo");

def saludoNombre(request, nombre, edad):
    return HttpResponse(f"¡Hola {nombre} bienvenido a progra III!, tu edad es {edad}")

def index(request):
    return render(request, 'index.html')