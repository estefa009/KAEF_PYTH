from django.shortcuts import render,redirect

from sdnts.models import Usuario,Producto, Carrito, CarritoItem
from .forms import UsuarioForm  # El punto (.) indica que es desde la misma app
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Context processors
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
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Usamos los campos reales: email y passw_usua
        usuario = Usuario.objects.filter(email=email, passw_usua=password).first()

        if usuario:
            # Guardamos el ID del usuario en sesión
            request.session['cod_usuario'] = usuario.cod_usuario
            rol = usuario.rol.upper() if usuario.rol else ''

            # Redirección por rol
            if rol == 'ADMIN':
                return redirect('admin_dashboard')
            elif rol == 'CLIENTE':
                return redirect('vistacliente')  # Asegúrate de que esta ruta exista
            elif rol == 'DOMI':
                return redirect('domiciliario_envios')
            else:
                return redirect('error_view')
        else:
            return render(request, 'auth/login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'auth/login.html')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o a donde necesites
    else:
        form = UsuarioForm()
    
    return render(request, 'auth/registro.html', {'form': form})




class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset.html'
    extra_context = {'etapa': 'formulario'}

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password_reset.html'
    extra_context = {'etapa': 'correo_enviado'}

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password_reset.html'
    extra_context = {'etapa': 'nueva_contraseña'}

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password_reset.html'
    extra_context = {'etapa': 'completado'}
    
    
    
def vistacliente(request):
    return render(request, 'cliente/vistacliente.html') 

def catalogocliente(request):
    return render(request, 'cliente/catalogocliente.html')

def contactanoscliente(request):
    context = {
        'direccion': 'Cra 13 # 6510, Bogotá, Colombia',
        'horario': 'Lunes a Sábado 9:00 a.m - 6:00 p.m',
        'telefono': '+57 3026982043'
    }
    return render(request, 'cliente/contactanoscliente.html', context)
def nosotroscliente(request):
    return render(request, 'cliente/nosotroscliente.html')

def perfilcliente(request):
    return render(request, 'cliente/perfilcliente.html')


def agregar_al_carrito(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)
        masa = data.get('masa')
        cobertura = data.get('cobertura')
        topping = data.get('topping')
        
        producto = get_object_or_404(Producto, id=producto_id)
        
        if request.user.is_authenticated:
            carrito, created = Carrito.objects.get_or_create(usuario=request.user, completado=False)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            carrito, created = Carrito.objects.get_or_create(session_key=session_key, completado=False)
            request.session['session_key'] = session_key
        
        # Verificar si el producto ya está en el carrito
        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={
                'masa_seleccionada': masa,
                'cobertura_seleccionada': cobertura,
                'topping_seleccionado': topping,
                'cantidad': cantidad
            }
        )
        
        if not created:
            item.cantidad += int(cantidad)
            item.save()
        
        return JsonResponse({
            'success': True,
            'total_items': carrito.cantidad_items,
            'total_carrito': float(carrito.total)
        })
    
    return JsonResponse({'success': False})

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    item.delete()
    return redirect('ver_carrito')

def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, completado=False).first()
    else:
        session_key = request.session.get('session_key')
        carrito = Carrito.objects.filter(session_key=session_key, completado=False).first() if session_key else None
    
    return render(request, 'carrito.html', {'carrito': carrito})

def actualizar_carrito(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        cantidad = data.get('cantidad')
        
        item = get_object_or_404(CarritoItem, id=item_id)
        item.cantidad = cantidad
        item.save()
        
        return JsonResponse({
            'success': True,
            'subtotal': float(item.subtotal()),
            'total_carrito': float(item.carrito.total),
            'total_items': item.carrito.cantidad_items
        })
    
    return JsonResponse({'success': False})

