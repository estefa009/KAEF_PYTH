from django.shortcuts import render,redirect
from .forms import UsuarioForm  # El punto (.) indica que es desde la misma app

def nav_index(request):
    return render(request, 'includes/nav_index.html')

def nav_admin(request):
    return render(request, 'includes/nav_admin.html')

def nav_user(request):
    return render(request, 'includes/nav_user.html')


# Create your views here.
def index(request):
    return render(request, 'index/index.html')

def catalogo(request):
    return render(request, 'index/catalogo.html')

def contactanos(request):
    context = {
        'direccion': 'Cra 13 # 6510, Bogotá, Colombia',
        'horario': 'Lunes a Sábado 9:00 a.m - 6:00 p.m',
        'telefono': '+57 3026982043'
    }
    return render(request, 'index/contactanos.html', context)
def nosotros(request):
    
    return render(request, 'index/nosotros.html')

def login(request):
    return render(request,'auth/login.html')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o a donde necesites
    else:
        form = UsuarioForm()
    
    return render(request, 'auth/registro.html', {'form': form})