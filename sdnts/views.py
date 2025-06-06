import base64
import openpyxl
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from sdnts.models import CategoriaInsumo, Entrada, Envio, Produccion, Proveedor, Salida, Usuario,Producto, Carrito, CarritoItem, Venta,Domiciliario
from .forms import UsuarioForm, PerfilForm  # El punto (.) indica que es desde la misma app
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import json
from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CargarDatosForm  # Asume que tienes este formulario creado
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from sdnts.models import SaborMasa, Glaseado, Topping, CombinacionProducto
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
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
        
        usuario = Usuario.objects.filter(email=email).first()

        if usuario and usuario.check_password(password):
            # Guardamos el ID del usuario en sesión
            request.session['cod_usuario'] = usuario.cod_usuario
            
            # También puedes iniciar sesión con Django si quieres
            auth_login(request, usuario)
            
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
    
    
def logout_view(request):
    logout(request)
    return redirect('login') 
    
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
    usuario = request.user  # usuario autenticado
    try:
        cliente = usuario.cliente  # acceso al modelo Cliente relacionado
    except:
        cliente = None  # por si no es un cliente (es admin u otro)

    contexto = {
        'usuario': usuario,
        'cliente': cliente,
    }
    return render(request, 'cliente/perfilcliente.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Procesar el formulario
        request.user.nom_usua = request.POST.get('nombre')
        request.user.apell_usua = request.POST.get('apellido')
        request.user.email = request.POST.get('email')
        request.user.tele_usua = request.POST.get('telefono')
        request.user.cliente.direc_cliente = request.POST.get('direccion')
        
        try:
            request.user.save()
            request.user.cliente.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfilcliente')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    # Para la Opción 2:
    editando = request.GET.get('editar') == '1'
    
    return render(request, 'cliente/editar_perfil.html' if not editando else 'perfilcliente.html', {
        'user': request.user,
        'editando': editando  # Solo para Opción 2
    })


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
    carrito = item.carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, completado=False).first()
    else:
        session_key = request.session.get('session_key')
        carrito = Carrito.objects.filter(session_key=session_key, completado=False).first() if session_key else None
    
    return render(request, 'includes/carrito.html', {'carrito': carrito})

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

@login_required
def mis_domicilios(request):
    try:
        domiciliario = request.user.domiciliario  # Obtener el domiciliario vinculado al usuario
        envios = Envio.objects.filter(domiciliario=domiciliario, estado='PENDIENTE')  # O el estado que desees filtrar
    except Domiciliario.DoesNotExist:
        messages.error(request, "No tienes un perfil de domiciliario asignado.")
        envios = []

    return render(request, 'domiciliario/mis_domicilios.html', {'envios': envios})
   
@login_required
def historial_envios(request):
    usuario = request.user  # Asegúrate de usar autenticación
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')
    
    envios = Envio.objects.filter(domiciliario__usuario=usuario)

    if fecha_desde:
        envios = envios.filter(fecha_hora_entrega__date__gte=fecha_desde)
    if fecha_hasta:
        envios = envios.filter(fecha_hora_entrega__date__lte=fecha_hasta)

    return render(request, 'domiciliario/historial_envios.html', {
        'envios': envios,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    })
    



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



def reporte_usuarios_pdf(request):
    # Estadísticas: contar cuántos usuarios hay por rol
    roles = ['ADMIN', 'CLIENTE', 'DOMI']
    conteo_roles = [Usuario.objects.filter(rol=rol).count() for rol in roles]

    # Generar gráfico con matplotlib
    plt.figure(figsize=(6, 4))
    plt.bar(roles, conteo_roles, color=['red', 'blue', 'green'])
    plt.title('Usuarios por Rol')
    plt.xlabel('Rol')
    plt.ylabel('Cantidad')

    # Guardar gráfico en memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    grafico_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Renderizar template HTML con gráfico embebido
    html_string = render_to_string('reportes/usuarios_pdf.html', {
        'grafico_base64': grafico_base64,
        'total_admin': conteo_roles[0],
        'total_cliente': conteo_roles[1],
        'total_domi': conteo_roles[2],
    })

    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # Devolver PDF como respuesta
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_usuarios.pdf"'
    return response



def reporte_usuarios_excel(request):
    # Crear libro de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Usuarios"

    # Cabeceras
    ws.append(['ID', 'Nombre', 'Apellido', 'Email', 'Rol', 'Activo'])

    # Llenar filas con los datos
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        ws.append([
            usuario.pk,
            usuario.nomUsua,
            usuario.apellUsua,
            usuario.emailUsua,
            usuario.rol,
            "Sí" if usuario.activo else "No"
        ])

    # Preparar respuesta
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=usuarios.xlsx'
    wb.save(response)

    return response

def guardar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nomUsua']
        apellido = request.POST['apellUsua']
        email = request.POST['emailUsua']
        password = request.POST['passwUsua']
        rol = request.POST['rol']
        activo = request.POST['activo']

        # Aquí va tu lógica para guardar el usuario
        print(nombre, apellido, email, password, rol, activo)

        return redirect('/')  # redirige a donde quieras
    
    
def actualizar_usuario(request):
    if request.method == 'POST':
        cod_usuario = request.POST.get('codUsuario')
        nombre = request.POST.get('nomUsua')
        apellido = request.POST.get('apellUsua')
        email = request.POST.get('emailUsua')
        rol = request.POST.get('rol')

        usuario = get_object_or_404(Usuario, pk=cod_usuario)
        usuario.nom_usua = nombre
        usuario.apell_usua = apellido
        usuario.email_usua = email
        usuario.rol = rol
        usuario.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la misma página
    
def eliminar_usuario(request, cod_usuario):
      usuario = get_object_or_404(Usuario, pk=cod_usuario)
      usuario.delete()
      return redirect(request.META.get('HTTP_REFERER', '/')) 