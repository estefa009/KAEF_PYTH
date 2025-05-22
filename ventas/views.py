from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def contactanos(request):
    context = {
        'direccion': 'Cra 13 # 6510, Bogotá, Colombia',
        'horario': 'Lunes a Sábado 9:00 a.m - 6:00 p.m',
        'telefono': '+57 3026982043'
    }
    return render(request, 'contactanos.html', context)
def nosotros(request):
    
    return render(request, 'nosotros.html')