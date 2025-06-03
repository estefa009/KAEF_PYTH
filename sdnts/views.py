from django.shortcuts import render,redirect

from sdnts.models import CategoriaInsumo, Entrada, Envio, Produccion, Proveedor, Salida, Usuario,Producto, Carrito, CarritoItem, Venta
from .forms import UsuarioForm  # El punto (.) indica que es desde la misma app
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CargarDatosForm  # Asume que tienes este formulario creado

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
                return redirect('dashboard')
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

<<<<<<< HEAD
def domiciliario_envios(request):
    return render(request, 'domi/domiciliario_envios.html') 


@login_required
def dashboard(request):
    # Datos para las tarjetas resumen
    total_usuarios = Usuario.objects.count()
    # ✅ Corregido: usar 'fecha_hora' en lugar de 'fecha'
    ventas_recientes = Venta.objects.order_by('-fecha_hora')[:5]
    # ✅ Corregido: usar 'fecha_inicio' en lugar de 'fecha'
    produccion_reciente = Produccion.objects.order_by('-fecha_inicio')[:3]
    
    context = {
        'total_usuarios': total_usuarios,
        'ventas_recientes': ventas_recientes,
        'produccion_reciente': produccion_reciente,
    }
    return render(request, 'admin/dashboard.html', context)

# Vista de Ventas
@login_required
def ventas(request):
    # ✅ Corregido: usar 'fecha_hora' en lugar de 'fecha'
    ventas = Venta.objects.all().order_by('-fecha_hora')
    # ✅ Corregido: usar 'total' en lugar de 'monto'
    total_ventas = ventas.aggregate(sum('total'))['total__sum'] or 0
    
    return render(request, 'admin/ventas.html', {
        'ventas': ventas,
        'total_ventas': total_ventas
    })

# Vista de Producción
@login_required
def produccion(request):
    # ✅ Corregido: usar 'fecha_inicio' en lugar de 'fecha'
    producciones = Produccion.objects.all().order_by('-fecha_inicio')
    return render(request, 'admin/produccion.html', {'producciones': producciones})

# Vista de Envíos
@login_required
def envios(request):
    envios_pendientes = Envio.objects.filter(estado='PENDIENTE')
    # ✅ Corregido: usar 'ENTREGADO' en lugar de 'COMPLETADO'
    envios_completados = Envio.objects.filter(estado='ENTREGADO')
    
    return render(request, 'admin/envios.html', {
        'envios_pendientes': envios_pendientes,
        'envios_completados': envios_completados
    })

# Vista de Proveedores
@login_required
def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'admin/proveedores.html', {'proveedores': proveedores})

# Vista de Entradas (Inventario)
@login_required
def entradas(request):
    # ✅ Corregido: usar el modelo 'Entrada' directamente
    entradas = Entrada.objects.all().order_by('-fecha_hora_entrada')
    return render(request, 'admin/entradas.html', {'entradas': entradas})

# Vista de Salidas (Inventario)
@login_required
def salidas(request):
    # ✅ Corregido: usar el modelo 'Salida' directamente
    salidas = Salida.objects.all().order_by('-fecha_hora_salida')
    return render(request, 'admin/salidas.html', {'salidas': salidas})

# Vista de Categorías
@login_required
def categorias(request):
    # ✅ Corregido: usar 'CategoriaInsumo' en lugar de 'Categoria'
    categorias = CategoriaInsumo.objects.all()
    return render(request, 'admin/categorias.html', {'categorias': categorias})

# Vista de Correos - COMENTADA porque no tienes este modelo
# Si necesitas esta funcionalidad, debes crear el modelo Correo
"""
@login_required
def correos(request):
    # ❌ El modelo 'Correo' no existe en tu models.py
    # Necesitas crear este modelo o eliminar esta vista
    correos_enviados = Correo.objects.all().order_by('-fecha_envio')
    return render(request, 'admin/correos.html', {'correos': correos_enviados})
"""

# Vista para Cargar Datos
@login_required
def cargarDatos(request):
    if request.method == 'POST':
        form = CargarDatosForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesar el archivo subido
            archivo = request.FILES['archivo']
            # Aquí iría tu lógica para procesar el archivo
            return redirect('dashboard')
    else:
        form = CargarDatosForm()
    
    return render(request, 'admin/cargarDatos.html', {'form': form})

# 🔥 VISTAS ADICIONALES QUE PODRÍAS NECESITAR

@login_required
def insumos(request):
    """Vista para gestionar insumos"""
    from .models import Insumo
    insumos = Insumo.objects.select_related('cod_categoria').all()
    return render(request, 'admin/insumos.html', {'insumos': insumos})

@login_required
def productos(request):
    """Vista para gestionar productos"""
    productos = Producto.objects.all()
    return render(request, 'admin/productos.html', {'productos': productos})

@login_required
def clientes(request):
    """Vista para gestionar clientes"""
    from .models import Cliente
    clientes = Cliente.objects.select_related('cod_usua').all()
    return render(request, 'admin/clientes.html', {'clientes': clientes})

@login_required
def domiciliarios(request):
    """Vista para gestionar domiciliarios"""
    from .models import Domiciliario
    domiciliarios = Domiciliario.objects.select_related('cod_usua').all()
    return render(request, 'admin/domiciliarios.html', {'domiciliarios': domiciliarios})

def correos(request):
    """Vista para mostrar la página de correos"""
    return render(request, 'admin/correos.html')
=======
>>>>>>> 43730b0fff9afea16ed7181adc564a0838f2e701
