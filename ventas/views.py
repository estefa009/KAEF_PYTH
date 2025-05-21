from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def contactanos(request):
    return render(request, 'contactanos.html')

def nosotros(request):
    return render(request, 'nosotros.html')