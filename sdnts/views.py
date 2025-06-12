#from .forms import UserProfileForm  # Agrega esta línea al inicio del archivo o antes de la vista
import base64
from datetime import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
import openpyxl
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from sdnts.models import CategoriaInsumo, DetalleVenta, Entrada, Envio, Produccion, Proveedor, Salida, Usuario,Producto, Carrito, CarritoItem, Venta,Domiciliario,Cliente,Pago
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
import json
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CargarDatosForm, PerfilAdminForm, CambiarContrasenaForm, RegistroUsuarioForm,UsuarioForm # Asume que tienes este formulario creado
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from sdnts.models import SaborMasa, Glaseado, Topping, CombinacionProducto, Usuario
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from django.db.models import Sum

from decimal import Decimal

from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import timedelta


from django.contrib.auth import get_user_model

# Context processors
def nav_index(request):
    return render(request, 'includes/nav_index.html')

def nav_admin(request):
    return render(request, 'includes/nav_admin.html')

def nav_user(request):
    return render(request, 'includes/nav_user.html')


# --- FUNCION NORMALIZAR PARA MAPEOS DE NOMBRES ---
def normalizar(nombre):
    if not nombre:
        return ''
    import unicodedata
    nombre = nombre.lower().strip()
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    nombre = nombre.replace('-', ' ').replace('_', ' ')
    nombre = nombre.replace('m&m', 'mm')
    return nombre

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
                return redirect('dashboard_admin')
            elif rol == 'CLIENTE':
                return redirect('vistacliente')  
            elif rol == 'DOMI':
                return redirect('mis_domicilios')
            else:
                return redirect('error_view')
        else:
            return render(request, 'auth/login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'auth/login.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)  # Este formulario NO tiene campo 'rol'
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.rol = 'CLIENTE'  # Asigna el rol por defecto
            usuario.save()
            enviar_correo_bienvenida(usuario)
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'auth/registro.html', {'form': form})


@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)  # Este formulario SÍ tiene campo 'rol'
        if form.is_valid():
            usuario = form.save()
            enviar_correo_bienvenida_admin(usuario)
            messages.success(request, "Usuario agregado exitosamente.")
            return redirect('dashboard_admin')
        else:
         messages.error(request, 'Corrige los errores en el formulario.')
    else: 
        form = UsuarioForm()
    return render(request, 'usuario/agregar_usuario.html', {'form': form})


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
        
    
def enviar_correo_bienvenida(usuario):
    asunto = '¡Bienvenido a StefasDonuts!'
    mensaje_html = f'''
    <h2>Hola {usuario.nom_usua}!</h2>
    <p>Te damos la bienvenida a <strong>StefasDonutsm</strong>.</p>
    <p>Tus datos son:</p>
    <ul>
        <li><strong>Usuario:</strong> {usuario.nom_usua}</li>
        <li><strong>Email:</strong> {usuario.email}</li>
    </ul>
    <p>Puedes iniciar sesión aquí: 
        <a href="http://127.0.0.1:8000/{reverse('login')}">Iniciar sesión</a>
    </p>
    '''
    mensaje_texto = strip_tags(mensaje_html)  # Por si el cliente de correo no soporta HTML

    send_mail(
        asunto,
        mensaje_texto,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        html_message=mensaje_html
    )
    
def enviar_correo_bienvenida_admin(usuario):
    asunto = '¡Bienvenido a StefasDonuts!'
    mensaje_html = f'''
    <h2>Hola {usuario.nom_usua}!</h2>
    <p>Te damos la bienvenida a <strong>StefasDonuts</strong>.</p>
    <p>Tus datos son:</p>
    <ul>
        <li><strong>Usuario:</strong> {usuario.nom_usua}</li>
        <li><strong>Email:</strong> {usuario.email}</li>
        <li><strong>Rol asignado:</strong> {usuario.rol}</li>
    </ul>
    <p>Puedes iniciar sesión aquí: 
        <a href="http://127.0.0.1:8000{reverse('login')}">Iniciar sesión</a>
    </p>
    '''
    mensaje_texto = strip_tags(mensaje_html)
    send_mail(
        asunto,
        mensaje_texto,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        html_message=mensaje_html
    )
    
    
@login_required   
def logout_view(request):
    logout(request)
    return redirect('login') 
@login_required    
def vistacliente(request):
    return render(request, 'cliente/vistacliente.html') 
@login_required
def catalogocliente(request):
    masas = SaborMasa.objects.all()
    coberturas = Glaseado.objects.all()
    toppings = Topping.objects.all()

    # Obtener productos por tamaño
    producto_s = Producto.objects.filter(tamano='S', activo=True).first()
    producto_m = Producto.objects.filter(tamano='M', activo=True).first()
    producto_l = Producto.objects.filter(tamano='L', activo=True).first()
    producto_xl = Producto.objects.filter(tamano='XL', activo=True).first()

    return render(request, 'cliente/catalogocliente.html', {
        'masas': masas,
        'coberturas': coberturas,
        'toppings': toppings,
        'producto_s': producto_s,
        'producto_m': producto_m,
        'producto_l': producto_l,
        'producto_xl': producto_xl,
        # ...otros contextos...
    })
    return render(request, 'cliente/catalogocliente.html')

@login_required
def contactanoscliente(request):
    context = {
        'direccion': 'Cra 13 # 6510, Bogotá, Colombia',
        'horario': 'Lunes a Sábado 9:00 a.m - 6:00 p.m',
        'telefono': '+57 3026982043'
    }
    return render(request, 'cliente/contactanoscliente.html', context)
def nosotroscliente(request):
    return render(request, 'cliente/nosotroscliente.html')

@login_required
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
    
@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password1'])
            usuario.save()
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('dashboard_admin')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/agregar_usuario.html', {'form': form})

@login_required
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

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse

@login_required
@csrf_exempt
def procesar_compra(request):
    import traceback
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Datos recibidos en procesar_compra:', data)
            carrito = data.get('carrito', [])
            direccion = data.get('direccion', '')
            fecha_entrega = data.get('fecha_entrega')
            metodo_pago = data.get('metodo_pago', 'NEQUI')
            transaccion_id = data.get('transaccion_id', '')

            user = request.user if request.user.is_authenticated else None
            if not user:
                print('Usuario no autenticado')
                return JsonResponse({'success': False, 'error': 'Usuario no autenticado'})
            try:
                cliente = Cliente.objects.get(cod_usua=user)
            except Exception as e:
                print('No se encontró Cliente para el usuario:', user, e)
                return JsonResponse({'success': False, 'error': 'No se encontró Cliente para el usuario'})

            subtotal = sum(item['precio'] * item['quantity'] for item in carrito)
            iva = subtotal * 0.19
            total = subtotal + iva

            # 1. Crear la venta (sin fecha_entrega)
            venta = Venta.objects.create(
                cod_cliente=cliente,
                subtotal=subtotal,
                iva=iva,
                total=total,
                direccion_entrega=direccion,
                fecha_hora=timezone.now()
            )
            print('Venta creada:', venta)

            # 2. Crear los detalles de venta y combinaciones
            COBERTURA_MAP = {
                normalizar("Choco Blanco"): "Choc. Blanco",
                normalizar("Choc Blanco"): "Choc. Blanco",
                normalizar("Choc. Blanco"): "Choc. Blanco",
                normalizar("choc-blanco"): "Choc. Blanco",
                normalizar("Chocolate Blanco"): "Choc. Blanco",  # <-- Agregado
                normalizar("chocolate blanco"): "Choc. Blanco",  # <-- Agregado
                normalizar("Chocolate Oscuro"): "Choc. Oscuro",
                normalizar("Choc Oscuro"): "Choc. Oscuro",
                normalizar("Choc. Oscuro"): "Choc. Oscuro",
                normalizar("choc-oscuro"): "Choc. Oscuro",
                normalizar("Arequipe"): "Arequipe",
                # Agrega aquí todos los nombres posibles y sus variantes normalizadas
            }
            MASA_MAP = {
                normalizar("Vainilla"): "Vainilla",
                normalizar("Chocolate"): "Chocolate",
                normalizar("Red Velvet"): "Red Velvet",
                # Agrega aquí todos los nombres posibles y sus variantes normalizadas
            }
            TOPPING_MAP = {
                normalizar("Chispas"): "Chispas",
                normalizar("Oreo"): "Oreo",
                normalizar("M&M"): "M&M",
                normalizar("mm"): "M&M",
                normalizar("Chips"): "Chips",
                normalizar("Ninguno"): None,
                # Agrega aquí todos los nombres posibles y sus variantes normalizadas
            }
            for item in carrito:
                producto = Producto.objects.filter(cod_producto=item['cod_producto']).first()
                if not producto:
                    print('Producto no encontrado para cod_producto:', item['cod_producto'])
                    continue
                DetalleVenta.objects.create(
                    cod_venta=venta,
                    cod_producto=producto,
                    cantidad=item['quantity'],
                    precio_unitario=item['precio'],
                    fecha_entrega=fecha_entrega
                )
                print('DetalleVenta creado para producto:', producto)
                # Guardar la combinación personalizada
                masa_nombre = cobertura_nombre = topping_nombre = None
                try:
                    # --- MASA ---
                    masa_nombre = item['masa']['nombre']
                    masa_nombre_norm = normalizar(masa_nombre)
                    masa_nombre_db = MASA_MAP.get(masa_nombre_norm, masa_nombre)
                    masa = SaborMasa.objects.filter(nombre__iexact=masa_nombre_db).first()
                    if not masa:
                        masa = SaborMasa.objects.filter(nombre__icontains=masa_nombre_db).first()
                    if not masa:
                        print('No se encontró SaborMasa para:', masa_nombre, '| Normalizado:', masa_nombre_norm)
                        print('Nombres válidos en BD:', list(SaborMasa.objects.values_list('nombre', flat=True)))
                        raise Exception(f'SaborMasa no encontrado para "{masa_nombre}"')
                    # --- COBERTURA ---
                    cobertura_nombre = item['cobertura']['nombre']
                    cobertura_nombre_norm = normalizar(cobertura_nombre)
                    cobertura_nombre_db = COBERTURA_MAP.get(cobertura_nombre_norm, cobertura_nombre)
                    print(f'Buscando Glaseado en BD: "{cobertura_nombre_db}" (original: "{cobertura_nombre}", normalizado: "{cobertura_nombre_norm}")')
                    cobertura = Glaseado.objects.filter(nombre__iexact=cobertura_nombre_db).first()
                    if not cobertura:
                        cobertura = Glaseado.objects.filter(nombre__icontains=cobertura_nombre_db).first()
                    if not cobertura:
                        print('No se encontró Glaseado para:', cobertura_nombre, '| Normalizado:', cobertura_nombre_norm)
                        print('Nombres válidos en BD:', list(Glaseado.objects.values_list('nombre', flat=True)))
                        raise Exception(f'Glaseado no encontrado para "{cobertura_nombre}"')
                    # --- TOPPING ---
                    topping = None
                    topping_nombre = item['topping']['nombre']
                    topping_nombre_norm = normalizar(topping_nombre)
                    topping_nombre_db = TOPPING_MAP.get(topping_nombre_norm, topping_nombre)
                    if topping_nombre_db and topping_nombre_db.lower() != 'ninguno':
                        topping = Topping.objects.filter(nombre__iexact=topping_nombre_db).first()
                        if not topping:
                            topping = Topping.objects.filter(nombre__icontains=topping_nombre_db).first()
                        if not topping:
                            print('No se encontró Topping para:', topping_nombre, '| Normalizado:', topping_nombre_norm)
                            print('Nombres válidos en BD:', list(Topping.objects.values_list('nombre', flat=True)))
                            raise Exception(f'Topping no encontrado para "{topping_nombre}"')
                    CombinacionProducto.objects.create(
                        cod_venta=venta,
                        cod_producto=producto,
                        cod_sabor_masa_1=masa,
                        cod_glaseado_1=cobertura,
                        cod_topping_1=topping
                    )
                    print('CombinacionProducto creada')
                except Exception as e:
                    print(f'Error creando CombinacionProducto para producto {producto} (masa: {masa_nombre}, cobertura: {cobertura_nombre}, topping: {topping_nombre}):', e)

            # 3. Crear el pago
            Pago.objects.create(
                cod_venta=venta,
                metodo_pago=metodo_pago,
                monto_total=total,
                fecha_hora_pago=timezone.now(),
                estado_pago='PENDIENTE',
                transaccion_id=transaccion_id
            )
            print('Pago creado')

            # 4. Preparar detalles para la respuesta
            detalles = DetalleVenta.objects.filter(cod_venta=venta)
            detalle_list = []
            for d in detalles:
                detalle_list.append({
                    'producto': d.cod_producto.nomb_pro,
                    'cantidad': d.cantidad,
                    'precio_unitario': float(d.precio_unitario),
                    'subtotal': float(d.precio_unitario) * d.cantidad
                })

            return JsonResponse({
                'success': True,
                'venta': {
                    'fecha': venta.fecha_hora.strftime('%d/%m/%Y %H:%M:%S'),
                    'direccion': venta.direccion_entrega,
                    'subtotal': float(venta.subtotal),
                    'iva': float(venta.iva),
                    'total': float(venta.total),
                    'detalles': detalle_list
                }
            })
        except Exception as e:
            print('Error en procesar_compra:', e)
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})
            return JsonResponse({'success': False, 'error': 'Método no permitido'})
            carrito = data.get('carrito', [])
            direccion = data.get('direccion', '')  # Puedes pedirla en el modal
            observaciones = data.get('observaciones', '')
        except Exception:
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

        if not carrito:
            return JsonResponse({'success': False, 'error': 'Carrito vacío'}, status=400)

        try:
            cliente = request.user.cliente
        except Exception:
            return JsonResponse({'success': False, 'error': 'No es cliente'}, status=400)

        subtotal = Decimal('0.00')
        detalles = []

        for item in carrito:
            # Busca el producto por nombre y tamaño
            talla = item.get('talla')
            nombre = item.get('titulo')
            cantidad = int(item.get('quantity', 1))
            precio_unitario = Decimal(str(item.get('precio', 0)))
            try:
                producto = Producto.objects.get(nomb_pro=nombre, tamano=talla)
            except Producto.DoesNotExist:
                continue

            detalles.append({
                'producto': producto,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario,
            })
            subtotal += precio_unitario * cantidad

        iva = subtotal * Decimal('0.19')
        total = subtotal + iva

        venta = Venta.objects.create(
            cod_cliente=cliente,
            subtotal=subtotal,
            iva=iva,
            total=total,
            direccion_entrega=direccion,
            observaciones=observaciones
        )

        for det in detalles:
            DetalleVenta.objects.create(
                cod_venta=venta,
                cod_producto=det['producto'],
                cantidad=det['cantidad'],
                precio_unitario=det['precio_unitario']
            )

        return JsonResponse({
            'success': True,
            'venta': {
                'id': venta.cod_venta,
                'fecha': venta.fecha_hora.strftime('%Y-%m-%d %H:%M'),
                'subtotal': str(subtotal),
                'iva': str(iva),
                'total': str(total),
                'direccion': venta.direccion_entrega,
                'detalles': [
                    {
                        'producto': str(det['producto']),
                        'cantidad': det['cantidad'],
                        'precio_unitario': str(det['precio_unitario']),
                        'subtotal': str(det['precio_unitario'] * det['cantidad'])
                    }
                    for det in detalles
                ]
            }
        })

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def exportar_excel(request):
    usuario = request.user
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    envios = Envio.objects.filter(domiciliario__usuario=usuario)
    if fecha_desde:
        envios = envios.filter(fecha_hora_entrega__date__gte=fecha_desde)
    if fecha_hasta:
        envios = envios.filter(fecha_hora_entrega__date__lte=fecha_hasta)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Código", "Fecha Entrega", "Tarifa", "Estado"])

    for envio in envios:
        ws.append([envio.cod_envio, str(envio.fecha_hora_entrega), envio.tarifa, envio.estado])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="historial_envios.xlsx"'
    wb.save(response)
    return response

    
@login_required    
def exportar_pdf(request):
    usuario = request.user
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')

    envios = Envio.objects.filter(cod_domi=usuario.domiciliario).order_by('fecha_entrega')

    if fecha_desde not in [None, '', 'None']:
        envios = envios.filter(fecha_entrega__date__gte=fecha_desde)

    if fecha_hasta not in [None, '', 'None']:
        envios = envios.filter(fecha_entrega__date__lte=fecha_hasta)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historial_envios.pdf"'

    p = canvas.Canvas(response)
    y = 800
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Historial de Envíos")
    y -= 30

    p.setFont("Helvetica", 10)
    for envio in envios:
        fecha_str = envio.fecha_entrega.strftime("%Y-%m-%d %H:%M") if envio.fecha_entrega else "Sin entregar"
        p.drawString(100, y, f"{envio.cod_envio} | {fecha_str} | {envio.tarifa_envio} | {envio.estado}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
            p.setFont("Helvetica", 10)

    p.save()
    return response



class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


@login_required
def mis_domicilios(request):
    try:
        domiciliario = request.user.domiciliario
    except Domiciliario.DoesNotExist:
        messages.error(request, "No tienes un perfil de domiciliario asignado.")
        return render(request, 'domiciliario/mis_domicilios.html', {'envios': [], 'nuevos_envios': []})

    envios = Envio.objects.filter(cod_domi=domiciliario, estado='PENDIENTE')

    recientes = now() - timedelta(days=1)
    nuevos_envios = Envio.objects.filter(
        cod_domi=domiciliario,
        fecha_asignacion__gte=recientes
    )

    context = {
        'envios': envios,
        'nuevos_envios': nuevos_envios,
    }

    return render(request, 'domiciliario/mis_domicilios.html', context)
 
@login_required
def historial_envios(request):
    usuario = request.user  # Asegúrate de usar autenticación
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')
    
    envios = Envio.objects.filter(cod_domi= request.user.domiciliario).order_by('fecha_entrega')

    nuevos_envios = Envio.objects.filter(
    cod_domi=usuario.domiciliario,
    fecha_asignacion__gte=timezone.now() - timedelta(days=1)
    ).order_by('-fecha_asignacion')


    return render(request, 'domiciliario/historial_envios.html', {
        'envios': envios,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'nuevos_envios': nuevos_envios,  # ✅ se pasa al template
    })
    
@login_required
def perfildomi(request):
    user = request.user
    return render(request, 'domiciliario/perfildomi.html', {'user': user})


User = get_user_model()

@login_required
def editar_perfildomi(request):
    user = request.user

    if request.method == 'POST':
        nom_usua = request.POST.get('nom_usua', user.nom_usua)
        apell_usua = request.POST.get('apell_usua', user.apell_usua)
        tele_usua = request.POST.get('tele_usua', user.tele_usua)
        email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        # Validación: verificar si el email ya existe y no es el del usuario actual
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'El correo electrónico ya está en uso.')
            return redirect('perfildomi')

        # Validación: confirmar contraseña si se escribe
        if password:
            if password != password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('perfildomi')
            user.set_password(password)
            update_session_auth_hash(request, user)

        # Guardar datos
        user.nom_usua = nom_usua
        user.apell_usua = apell_usua
        user.tele_usua = tele_usua
        user.email = email
        user.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfildomi')

    return render(request, 'domiciliario/editar_perfildomi.html', {'user': user})


#administrador
@login_required
def editar_usuario(request, cod_usuario):
    usuario = get_object_or_404(Usuario, cod_usuario=cod_usuario)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('dashboard_admin')  # Redirige al dashboard admin
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuario/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario agregado exitosamente.")
            return redirect('dashboard_admin')  # Redirige al dashboard admin
    else:
        form = UsuarioForm()

    return render(request, 'usuario/agregar_usuario.html', {'form': form})

@login_required
def dashboard_admin(request):
    total_usuarios = Usuario.objects.count()
    ventas_recientes = Venta.objects.order_by('-fecha_hora')[:5]
    produccion_reciente = Produccion.objects.order_by('-fecha_inicio')[:3]

    rol = request.GET.get('rol')  # Captura el rol desde el formulario

    if rol:
        usuarios = Usuario.objects.filter(rol=rol)
    else:
        usuarios = Usuario.objects.all()

    context = {
        'total_usuarios': total_usuarios,
        'ventas_recientes': ventas_recientes,
        'produccion_reciente': produccion_reciente,
        'usuarios': usuarios,
        'rol_actual': rol,  # para mantener el filtro seleccionado
    }

    return render(request, 'admin/dashboard_admin.html', context)


@login_required
def perfil_admin(request):
    usuario = request.user
    return render(request, 'admin/perfil_admin.html', {'usuario': usuario})

@login_required
def editarperfil_admin(request):
    usuario = request.user
    perfil_form = PerfilAdminForm(instance=usuario)
    password_form = CambiarContrasenaForm(user=usuario)

    if request.method == 'POST':
        if 'guardar_perfil' in request.POST:
            perfil_form = PerfilAdminForm(request.POST, instance=usuario)
            if perfil_form.is_valid():
                perfil_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('perfil_admin')
        
        elif 'cambiar_contrasena' in request.POST:
            password_form = CambiarContrasenaForm(user=usuario, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # para que no cierre la sesión
                messages.success(request, 'Contraseña cambiada correctamente.')
                return redirect('perfil_admin')
            else:
                messages.error(request, 'Corrige los errores en el formulario de contraseña.')

    return render(request, 'admin/editarperfil_admin.html', {
        'perfil_form': perfil_form,
        'password_form': password_form
    })
    
# Vista de Ventas
from django.core.paginator import Paginator
from django.db.models import Sum

@login_required
def ventas_admin(request):
    ventas_list = Venta.objects.all().order_by('-fecha_hora')

    # Paginación
    paginator = Paginator(ventas_list, 10)  # 10 ventas por página
    page_number = request.GET.get('page', 1)
    ventas = paginator.get_page(page_number)

    # Estadísticas
    ventas_pendientes = Venta.objects.filter(estado='PENDIENTE').count()
    ventas_en_camino = Venta.objects.filter(estado='EN_CAMINO').count()
    ventas_entregadas = Venta.objects.filter(estado='ENTREGADO').count()

    total_ventas = ventas_list.aggregate(Sum('total'))['total__sum'] or 0

    context = {
        'ventas': ventas,
        'total_ventas': total_ventas,
        'ventasPendientes': ventas_pendientes,
        'ventasEnCamino': ventas_en_camino,
        'ventasEntregadas': ventas_entregadas,
        'pagina_actual': ventas.number,
        'total_paginas': paginator.num_pages,
        'range_paginas': range(1, paginator.num_pages + 1),
    }

    return render(request, 'admin/ventas/ventas_admin.html', context)

from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Venta, DetalleVenta, Pago, CombinacionProducto
from .forms import VentaForm, DetalleVentaForm, PagoForm, CombinacionProductoForm
from django.db import transaction
from  decimal import Decimal
def agregar_venta_completa(request):
    DetalleFormSet = modelformset_factory(DetalleVenta, form=DetalleVentaForm, extra=1)
    CombinacionFormSet = modelformset_factory(CombinacionProducto, form=CombinacionProductoForm, extra=1)

    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST, prefix='detalle')
        combinacion_formset = CombinacionFormSet(request.POST, prefix='combo')
        pago_form = PagoForm(request.POST)

        if venta_form.is_valid() and detalle_formset.is_valid() and pago_form.is_valid() and combinacion_formset.is_valid():
            with transaction.atomic():
                venta = venta_form.save(commit=False)

                # Calcular totales
                subtotal = sum([
                    form.cleaned_data['precio_unitario'] * form.cleaned_data['cantidad']
                    for form in detalle_formset
                ])
                iva = subtotal * Decimal (0.19)
                total = subtotal + iva

                venta.subtotal = subtotal
                venta.iva = iva
                venta.total = total
                venta.save()

                for form in detalle_formset:
                    detalle = form.save(commit=False)
                    detalle.cod_venta = venta
                    detalle.save()

                for form, detalle_form in zip(combinacion_formset, detalle_formset):
                    combinacion = form.save(commit=False)
                    combinacion.cod_venta = venta
                    combinacion.cod_producto = detalle_form.cleaned_data['cod_producto']
                    combinacion.save()

                pago = pago_form.save(commit=False)
                pago.cod_venta = venta
                pago.monto_total = total
                pago.save()

            return redirect('ventas_admin')

    else:
        venta_form = VentaForm()
        detalle_formset = DetalleFormSet(queryset=DetalleVenta.objects.none(), prefix='detalle')
        combinacion_formset = CombinacionFormSet(queryset=CombinacionProducto.objects.none(), prefix='combo')
        pago_form = PagoForm()

    return render(request, 'admin/ventas/agregar_venta_completa.html', {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
        'combinacion_formset': combinacion_formset,
        'pago_form': pago_form,
        'productos': Producto.objects.all(), 
    })

@login_required
def detalle_ventas(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    detalles = DetalleVenta.objects.filter(cod_venta=venta).select_related('cod_producto')

    total = sum(detalle.subtotal for detalle in detalles)

    context = {
        'venta': venta,
        'detalles': detalles,
        'total': total,
    }
    return render(request, 'admin/ventas/detalle_ventas.html', context)

@login_required
def editar_estado_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Venta.ESTADOS).keys():
            venta.estado = nuevo_estado
            venta.save()
            return redirect('ventas_admin')

    return render(request, 'admin/ventas/editar_estado_venta.html', {
        'venta': venta,
        'estados': Venta.ESTADOS
    })


# Vista de Producción
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produccion, Salida, Entrada, Insumo, Venta, Envio
from .forms import ProduccionForm, SalidaForm, EntradaForm, EnvioForm
from django.db import transaction
@login_required
def produccion_admin(request):
    producciones = Produccion.objects.select_related('cod_venta').all()
    return render(request, 'admin/produccion/produccion_admin.html', {'producciones': producciones})


def crear_produccion(request):
    if request.method == 'POST':
        form = ProduccionForm(request.POST)
        salida_form = SalidaForm(request.POST)
        if form.is_valid() and salida_form.is_valid():
            with transaction.atomic():
                produccion = form.save()
                # Cambiar estado de la venta asociada
                venta = produccion.cod_venta
                venta.estado = 'PREPARACION' 
                venta.save()
                salida = salida_form.save(commit=False)
                salida.cod_produccion = produccion
                insumo = salida.cod_insumo
                if insumo.cnt_insumo >= salida.cantidad:
                    insumo.cnt_insumo -= salida.cantidad
                    insumo.save()
                    salida.save()
                else:
                    entrada = Entrada(
                        cod_insumo=insumo,
                        cnt_entrada=salida.cantidad - insumo.cnt_insumo,
                        precio_entrada=insumo.precio,
                        fecha_caducidad=None,
                        nom_entrada=f"Auto recarga para producción {produccion.cod_produccion}"
                    )
                    entrada.save()
                    insumo.cnt_insumo += entrada.cnt_entrada - salida.cantidad
                    insumo.save()
                    salida.save()
            return redirect('produccion_admin')
    else:
        form = ProduccionForm()
        salida_form = SalidaForm()
    return render(request, 'admin/produccion/crear_produccion.html', {'form': form, 'salida_form': salida_form})

def editar_produccion(request, cod_produccion):
    produccion = get_object_or_404(Produccion, pk=cod_produccion)
    if request.method == 'POST':
        form = ProduccionForm(request.POST, instance=produccion)
        if form.is_valid():
            form.save()
            return redirect('produccion_admin')
    else:
        form = ProduccionForm(instance=produccion)
    return render(request, 'admin/produccion/editar_produccion.html', {'form': form, 'produccion': produccion})

def cambiar_estado_produccion(request,cod_produccion ):
    produccion = get_object_or_404(Produccion, pk=cod_produccion)
    if request.method == 'POST':
        nuevo = request.POST.get('estado')
        if nuevo in dict(Produccion.ESTADOS):
            produccion.estado = nuevo
            if nuevo == 'FINALIZADO':
                produccion.fecha_fin = timezone.now()
            produccion.save()
        return redirect('produccion_admin')
    # Actualizar el estado de la venta asociada según el estado de la producción
    venta = produccion.cod_venta
    if produccion.estado == 'EN_PROCESO':
        venta.estado = 'PREPARACION'
    elif produccion.estado == 'FINALIZADO':
        venta.estado = 'EN_CAMINO'  
    elif produccion.estado == 'PENDIENTE':
        venta.estado = 'PENDIENTE'
    venta.save()
    return render(request, 'admin/produccion/cambiar_estado_produccion.html', {'produccion': produccion, 'estados': Produccion.ESTADOS})

def asignar_envio_produccion(request, cod_produccion):
    venta = get_object_or_404(Venta, cod_venta=cod_produccion)
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            envio = form.save(commit=False)
            envio.cod_venta = venta
            envio.fecha_asignacion = timezone.now()
            envio.estado = 'ASIGNADO'
            envio.save()
            return redirect('produccion_admin')
    else:
        form = EnvioForm()
    return render(request, 'admin/produccion/asignar_envio_produccion.html', {'form': form, 'venta': venta})

def eliminar_produccion(request, cod_produccion):
    produccion = get_object_or_404(Produccion, pk=cod_produccion)
    if request.method == 'POST':
        produccion.delete()
        return redirect('produccion_admin')
    return render(request, 'admin/produccion/eliminar_produccion.html', {'produccion': produccion})

#Envio Admin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Envio
from .forms import EnvioForm

# Vista de Envíos
@login_required
def envios_admin(request):
    envios = Envio.objects.all()
    return render(request, 'admin/envios/envios_admin.html', {'envios': envios})

def crear_envio(request):
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('envios_admin')
    else:
        form = EnvioForm()
    return render(request, 'admin/envios/crear_envio.html', {'form': form, 'titulo': 'Asignar Envío'})

def editar_envio(request, pk):
    envio = get_object_or_404(Envio, pk=pk)
    if request.method == 'POST':
        form = EnvioForm(request.POST, instance=envio)
        if form.is_valid():
            form.save()
            return redirect('envios_admin')
    else:
        form = EnvioForm(instance=envio)
    return render(request, 'admin/envios/editar_envio.html', {'form': form, 'titulo': 'Editar Envío'})

def eliminar_envio(request, pk):
    envio = get_object_or_404(Envio, pk=pk)
    envio.delete()
    return redirect('envios_admin')






# Vista de Proveedores
from .models import Proveedor
from .forms import ProveedorForm
@login_required
def proveedores_admin(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'admin/proveedores/proveedores_admin.html', {'proveedores': proveedores})


def agregar_proveedores(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nom_proveedor=request.POST['nom_proveedor'],
            telefono_proveedor=request.POST['telefono_proveedor'],
            direccion_proveedor=request.POST.get('direccion_proveedor', ''),
            email_proveedor=request.POST.get('email_proveedor', ''),
            novedad_proveedor=request.POST.get('novedad_proveedor', '')
        )
        return redirect('proveedores_admin')
    return render(request, 'admin/proveedores/agregar_proveedores.html')
    
def editar_proveedores(request, cod_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=cod_proveedor)
    if request.method == 'POST':
        proveedor.nom_proveedor = request.POST['nom_proveedor']
        proveedor.telefono_proveedor = request.POST['telefono_proveedor']
        proveedor.direccion_proveedor = request.POST.get('direccion_proveedor', '')
        proveedor.email_proveedor = request.POST.get('email_proveedor', '')
        proveedor.novedad_proveedor = request.POST.get('novedad_proveedor', '')
        proveedor.save()
        return redirect('proveedores_admin')
    return render(request, 'admin/proveedores/editar_proveedores.html', {'proveedor': proveedor})


def eliminar_proveedores(request, cod_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=cod_proveedor)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedores_admin')
    return render(request, 'admin/proveedores/eliminar_proveedores.html', {'proveedor': proveedor})



# Vista de Entradas (Inventario)
@login_required
def entradas_admin(request):
    # ✅ Corregido: usar el modelo 'Entrada' directamente
    entradas = Entrada.objects.all().order_by('-fecha_hora_entrada')
    return render(request, 'admin/entradas_admin.html', {'entradas': entradas})

# Vista de Salidas (Inventario)
@login_required
def salidas_admin(request):
    # ✅ Corregido: usar el modelo 'Salida' directamente
    salidas = Salida.objects.all().order_by('-fecha_hora_salida')
    return render(request, 'admin/salidas_admin.html', {'salidas': salidas})

# Vista de Categorías
@login_required
def categorias_admin(request):
    # ✅ Corregido: usar 'CategoriaInsumo' en lugar de 'Categoria'
    categorias = CategoriaInsumo.objects.all()
    return render(request, 'admin/categorias_admin.html', {'categorias': categorias})

# Vista de Correos - COMENTADA porque no tienes este modelo
# Si necesitas esta funcionalidad, debes crear el modelo Correo

@login_required
def correos_admin(request):
    from .models import Correo  # Asegúrate de que este modelo exista
    correos_enviados = Correo.objects.all().order_by('-fecha_envio')
    return render(request, 'admin/correos_admin.html', {'correos': correos_enviados})


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
def insumos_admin(request):
    """Vista para gestionar insumos"""
    from .models import Insumo
    insumos = Insumo.objects.select_related('cod_categoria').all()
    return render(request, 'admin/insumos_admin.html', {'insumos': insumos})

@login_required
def productos_admin(request):
    """Vista para gestionar productos"""
    productos = Producto.objects.all()
    return render(request, 'admin/productos_admin.html', {'productos': productos})

@login_required
def clientes_admin(request):
    """Vista para gestionar clientes"""
    from .models import Cliente
    clientes = Cliente.objects.select_related('cod_usua').all()
    return render(request, 'admin/clientes_admin.html', {'clientes': clientes})

@login_required
def domiciliarios_admin(request):
    """Vista para gestionar domiciliarios"""
    from .models import Domiciliario
    domiciliarios = Domiciliario.objects.select_related('cod_usua').all()
    return render(request, 'admin/domiciliarios_admin.html', {'domiciliarios': domiciliarios})


def reporte_usuarios_pdf(request):
    # Estadísticas: contar cuántos usuarios hay por rol
    roles = ['ADMIN', 'CLIENTE', 'DOMI']
    conteo_roles = [Usuario.objects.filter(rol=rol).count() for rol in roles]

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
      return redirect(request.META.get('HTTP_REFERER', '/'))

