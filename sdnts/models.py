from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        if not extra_fields.get('nom_usua'):
            raise ValueError('El nombre es obligatorio')
        if not extra_fields.get('apell_usua'):
            raise ValueError('El apellido es obligatorio')
        if not extra_fields.get('tele_usua'):
            raise ValueError('El teléfono es obligatorio')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('DOMI', 'Domiciliario'),
    )

    cod_usuario = models.AutoField(primary_key=True)
    email = models.EmailField('correo electrónico', unique=True)
    nom_usua = models.CharField('nombre', max_length=15, blank=False, null=False)
    apell_usua = models.CharField('apellido', max_length=20, blank=False, null=False)
    tele_usua = models.CharField('teléfono', max_length=15, blank=False, null=False)
    rol = models.CharField('rol', max_length=7, choices=ROLES, default='CLIENTE')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_usua', 'apell_usua', 'tele_usua']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nom_usua} {self.apell_usua}"
    
class Administrador(models.Model):
    """
    Modelo para administradores que extiende al usuario base
    """
    ESTADOS = (
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    )
    
    cod_admin = models.AutoField(primary_key=True)
    cod_usua = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='administrador'
    )
    estado_admin = models.CharField(
        'estado', 
        max_length=8, 
        choices=ESTADOS
    )
    
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
    
    def __str__(self):
        return f"Admin {self.cod_usua.nom_usua}"

class Cliente(models.Model):
    """
    Modelo para clientes que extiende al usuario base
    """
    cod_cliente = models.AutoField(primary_key=True)
    cod_usua = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='cliente'
    )
    direc_cliente = models.CharField('dirección', max_length=50)
    historial_compras = models.IntegerField('compras realizadas', default=0)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f'Cliente: {self.cod_usua.nom_usua} {self.cod_usua.apell_usua}'

class Domiciliario(models.Model):
    """
    Modelo para domiciliarios que extiende al usuario base
    """
    cod_domi = models.AutoField(primary_key=True)
    cod_usua = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='domiciliario'
    )
    disponibilidad = models.BooleanField('disponible', default=True)
    
    class Meta:
        verbose_name = 'Domiciliario'
        verbose_name_plural = 'Domiciliarios'
    
    def __str__(self):
        return f"Domiciliario {self.cod_usua.nom_usua}"

class Proveedor(models.Model):
    """
    Modelo para proveedores de insumos
    """
    cod_proveedor = models.AutoField(primary_key=True)
    nom_proveedor = models.CharField('nombre', max_length=50)
    telefono_proveedor = models.CharField('teléfono', max_length=13)
    direccion_proveedor = models.CharField('dirección', max_length=100, blank=True, null=True)
    email_proveedor = models.EmailField('correo', max_length=50, blank=True, null=True)
    novedad_proveedor = models.CharField('novedades', max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
    
    def __str__(self):
        return self.nom_proveedor

class CategoriaInsumo(models.Model):
    """
    Modelo para categorías de insumos
    """
    cod_categoria = models.AutoField(primary_key=True)
    nom_categoria = models.CharField('nombre', max_length=50, unique=True)
    descripcion = models.CharField('descripción', max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Categoría de Insumo'
        verbose_name_plural = 'Categorías de Insumos'
    
    def __str__(self):
        return self.nom_categoria

class Insumo(models.Model):
    """
    Modelo para insumos utilizados en la producción
    """
    cod_insumo = models.AutoField(primary_key=True)
    cod_categoria = models.ForeignKey(
        CategoriaInsumo,
        on_delete=models.CASCADE,
        related_name='insumos'
    )
    nomb_insumo = models.CharField('nombre', max_length=50)
    cnt_insumo = models.IntegerField('cantidad', default=0)
    unidad_medida = models.CharField('unidad de medida', max_length=10)
    
    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
    
    def __str__(self):
        return f"{self.nomb_insumo} ({self.cnt_insumo} {self.unidad_medida})"

class Entrada(models.Model):
    """
    Modelo para registrar entradas de insumos al inventario
    """
    cod_entrada = models.AutoField(primary_key=True)
    cod_insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name='entradas'
    )
    cod_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='entradas'
    )
    cnt_entrada = models.IntegerField('cantidad')
    precio_entrada = models.DecimalField('precio', max_digits=10, decimal_places=2)
    fecha_hora_entrada = models.DateTimeField('fecha de entrada', auto_now_add=True)
    fecha_caducidad = models.DateField('fecha de caducidad')    
    class Meta:
        verbose_name = 'Entrada de Insumo'
        verbose_name_plural = 'Entradas de Insumos'
    
    def __str__(self):
        return f"Entrada #{self.cod_entrada} - {self.cod_insumo.nomb_insumo}"

class Producto(models.Model):
    """
    Modelo para productos (donas) que se venden
    """
    TAMANOS = (
        ('S', 'Extra Pequeño'),
        ('M', 'Pequeño'),
        ('L', 'Mediano'),
        ('XL', 'Grande'),
    )
    MULTIPLICADORES_TAMANO = {
        'S': 1,
        'M': 2,
        'L': 3,
        'XL': 4,
    }

    cod_producto = models.AutoField(primary_key=True)
    nomb_pro = models.CharField('nombre', max_length=50, unique=True)
    tamano = models.CharField('tamaño', max_length=2, choices=TAMANOS)
    capacidad = models.IntegerField('capacidad', help_text='Cantidad de donas por bolsa')
    prec_pro = models.DecimalField('precio', max_digits=10, decimal_places=2)
    activo = models.BooleanField('activo', default=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def get_multiplicador(self):
        return self.MULTIPLICADORES_TAMANO.get(self.tamano, 1)

    def __str__(self):
        return f"{self.nomb_pro} ({self.get_tamano_display()})"

class Venta(models.Model):
    """
    Modelo para registrar ventas realizadas
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PREPARACION', 'En preparación'),
        ('EN_CAMINO', 'En camino'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    cod_venta = models.AutoField(primary_key=True)
    cod_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    fecha_hora = models.DateTimeField('fecha y hora', auto_now_add=True)
    subtotal = models.DecimalField('subtotal', max_digits=10, decimal_places=2)
    iva = models.DecimalField('IVA', max_digits=10, decimal_places=2)
    total = models.DecimalField('total', max_digits=10, decimal_places=2)
    estado = models.CharField(
        'estado',
        max_length=11,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    direccion_entrega = models.CharField('dirección de entrega', max_length=100)
    observaciones = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
    
    def __str__(self):
        return f"Venta #{self.cod_venta} - {self.cod_cliente}"

    def resumen_json(self):
        """
        Devuelve un resumen de la venta con toda la información relevante para el frontend.
        Incluye datos de pago y detalles de productos.
        """
        pago = getattr(self, 'pago', None)
        detalles = self.detalles.all()
        detalles_list = []
        for det in detalles:
            detalles_list.append({
                "producto": det.cod_producto.nomb_pro,
                "cantidad": det.cantidad,
                "precio_unitario": float(det.precio_unitario),
                "subtotal": float(det.subtotal),
                "fecha_entrega": det.fecha_entrega.strftime('%Y-%m-%d') if det.fecha_entrega else "",
                "descripcion": str(det.cod_producto)
            })
        return {
            "cod_venta": self.cod_venta,
            "fecha_hora": self.fecha_hora.strftime('%Y-%m-%d'),
            "subtotal": float(self.subtotal),
            "iva": float(self.iva),
            "total": float(self.total),
            "estado": self.estado,
            "direccion_entrega": self.direccion_entrega,
            "observaciones": self.observaciones,
            "metodo_pago": pago.metodo_pago if pago else "",
            "transaccion_id": pago.transaccion_id if pago else "",
            "detalles": detalles_list
        }

class DetalleVenta(models.Model):
    """
    Modelo para los detalles de productos en cada venta
    """
    cod_detalle = models.AutoField(primary_key=True)
    cod_venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    cod_producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='detalles_venta'
    )

    cantidad = models.IntegerField('cantidad', default=1)
    precio_unitario = models.DecimalField('precio unitario', max_digits=10, decimal_places=2)
    fecha_entrega = models.DateTimeField('fecha de entrega', default=timezone.now)  # <-- Obligatorio

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'
    
    @property 
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"Detalle #{self.cod_detalle} - Venta {self.cod_venta_id}"

class Pago(models.Model):
    """
    Modelo para registrar pagos de ventas
    """
    METODOS = (
        ('NEQUI', 'Nequi'),
        ('DAVIPLATA', 'Daviplata'),
    )
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('RECHAZADO', 'Rechazado'),
    )
    
    cod_pago = models.AutoField(primary_key=True)
    cod_venta = models.OneToOneField(
        Venta,
        on_delete=models.CASCADE,
        related_name='pago'
    )
    metodo_pago = models.CharField(
        'método de pago',
        max_length=9,
        choices=METODOS
    )
    monto_total = models.DecimalField('monto total', max_digits=10, decimal_places=2)
    fecha_hora_pago = models.DateTimeField('fecha y hora', auto_now_add=True)
    estado_pago = models.CharField(
        'estado',
        max_length=9,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    transaccion_id = models.CharField('ID de transacción', max_length=50, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
    
    def __str__(self):
        return f"Pago #{self.cod_pago} - {self.get_estado_pago_display()}"

class Produccion(models.Model):
    """
    Modelo para registrar el proceso de producción de pedidos
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('FINALIZADO', 'Finalizado'),
    )
    
    cod_produccion = models.AutoField(primary_key=True)
    cod_venta = models.OneToOneField(
        Venta,
        on_delete=models.CASCADE,
        related_name='produccion'
    )
    fecha_inicio = models.DateTimeField('fecha de inicio', auto_now_add=True)
    fecha_fin = models.DateTimeField('fecha de finalización', blank=True, null=True)
    estado = models.CharField(
        'estado',
        max_length=10,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    observaciones = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Producción'
        verbose_name_plural = 'Producciones'
    
    def __str__(self):
        return f"Producción #{self.cod_produccion} - {self.get_estado_display()}"

class Salida(models.Model):
    """
    Modelo para registrar salidas de insumos usados en producción
    """
    cod_salida = models.AutoField(primary_key=True)
    cod_produccion = models.ForeignKey(
        Produccion,
        on_delete=models.CASCADE,
        related_name='salidas'
    )
    cod_insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name='salidas'
    )
    cantidad = models.IntegerField('cantidad')
    fecha_hora_salida = models.DateTimeField('fecha y hora', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Salida de Insumo'
        verbose_name_plural = 'Salidas de Insumos'
    
    def __str__(self):
        return f"Salida #{self.cod_salida} - {self.cod_insumo.nomb_insumo}"

class Envio(models.Model):
    """
    Modelo para registrar envíos de pedidos
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('ASIGNADO', 'Asignado'),
        ('EN_CAMINO', 'En camino'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )
    
    cod_envio = models.AutoField(primary_key=True)
    cod_venta = models.OneToOneField(
        Venta,
        on_delete=models.CASCADE,
        related_name='envio'
    )
    cod_domi = models.ForeignKey(
        Domiciliario,
        on_delete=models.SET_NULL,
        related_name='envios',
        blank=True,
        null=True
    )
    fecha_asignacion = models.DateTimeField('fecha de asignación', blank=True, null=True)
    fecha_salida = models.DateTimeField('fecha de salida', blank=True, null=True)
    fecha_entrega = models.DateTimeField('fecha de entrega', blank=True, null=True)
    estado = models.CharField(
        'estado',
        max_length=10,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    tarifa_envio = models.DecimalField(
        'tarifa de envío',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    observaciones = models.CharField(max_length=200, blank=True, null=True)
    firma_recepcion = models.CharField('firma de recepción', max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Envío'
        verbose_name_plural = 'Envíos'
    
    def __str__(self):
        return f"Envío #{self.cod_envio} - {self.get_estado_display()}"

class SaborMasa(models.Model):
    cod_sabor_masa = models.AutoField(primary_key=True)
    nombre = models.CharField('nombre', max_length=30, unique=True)
    descripcion = models.CharField('descripción', max_length=100, blank=True, null=True)
    insumo = models.ForeignKey(
        'Insumo',
        on_delete=models.CASCADE,
        related_name='sabores_masa',  # <- diferente
        null=True, blank=True
    )
    def __str__(self):
        return self.nombre

class Glaseado(models.Model):
    TIPOS = (
        ('Oscuro', 'Oscuro'),
        ('Blanco', 'Blanco'),
        ('Colorido', 'Colorido'),
    )
    COLORES = (
        ('Rosado', 'Rosado'),
        ('Morado', 'Morado'),
        ('Naranja', 'Naranja'),
        ('Azul', 'Azul'),
        ('Verde', 'Verde'),
    )
    cod_glaseado = models.AutoField(primary_key=True)
    nombre = models.CharField('nombre', max_length=30)
    tipo = models.CharField('tipo', max_length=10, choices=TIPOS)
    color = models.CharField('color', max_length=10, choices=COLORES, blank=True, null=True)
    descripcion = models.CharField('descripción', max_length=100, blank=True, null=True)
    insumo = models.ForeignKey(
        'Insumo',
        on_delete=models.CASCADE,
        related_name='glaseados',  # <- diferente
        null=True, blank=True
    )
    def __str__(self):
        if self.tipo == 'Colorido':
            return f"{self.nombre} ({self.color})"
        return self.nombre

class Topping(models.Model):
    cod_topping = models.AutoField(primary_key=True)
    nombre = models.CharField('nombre', max_length=30, unique=True)
    descripcion = models.CharField('descripción', max_length=100, blank=True, null=True)
    insumo = models.ForeignKey(
        'Insumo',
        on_delete=models.CASCADE,
        related_name='toppings',  # <- diferente
        null=True, blank=True
    )
    def __str__(self):
        return self.nombre

class CombinacionProducto(models.Model):
    """
    Modelo para registrar las combinaciones personalizadas de productos en ventas
    """
    cod_combinacion = models.AutoField(primary_key=True)
    
    cod_venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='combinaciones'
    )
    cod_producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='combinaciones'
    )
    cod_detalle = models.ForeignKey(DetalleVenta, on_delete=models.CASCADE, related_name='combinaciones', null=True, blank=True)  # ← NUEVO

    # Primera combinación (obligatoria)
    cod_sabor_masa_1 = models.ForeignKey(
        SaborMasa,
        on_delete=models.CASCADE,
        related_name='combinaciones_primarias'
    )
    cod_glaseado_1 = models.ForeignKey(
        Glaseado,
        on_delete=models.CASCADE,
        related_name='combinaciones_primarias'
    )
    cod_topping_1 = models.ForeignKey(
        Topping,
        on_delete=models.SET_NULL,
        related_name='combinaciones_primarias',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Combinación de Producto'
        verbose_name_plural = 'Combinaciones de Productos'

    def __str__(self):
        return f"Combinación #{self.cod_combinacion} - Venta {self.cod_venta_id}"

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    
    @property
    def total(self):
        return sum(item.subtotal() for item in self.items.all())
    
    @property
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    masa_seleccionada = models.CharField(max_length=50, blank=True, null=True)
    cobertura_seleccionada = models.CharField(max_length=50, blank=True, null=True)
    topping_seleccionado = models.CharField(max_length=50, blank=True, null=True)
    
    def subtotal(self):
        return self.producto.prec_pro * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    
    
class Correo(models.Model):
        cod_correo = models.AutoField(primary_key=True)
        destinatario = models.EmailField('destinatario')
        asunto = models.CharField('asunto', max_length=200)
        mensaje = models.TextField('mensaje')
        fecha_envio = models.DateTimeField('fecha de envío', auto_now_add=True)
        enviado = models.BooleanField('enviado', default=False)
        
        class Meta:
            verbose_name = 'Correo'
            verbose_name_plural = 'Correos'
        
        def __str__(self):
            return f"Correo #{self.cod_correo} - {self.destinatario}"
        
class RecetaProducto(models.Model):
    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.DecimalField('cantidad necesaria', max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=10)

    class Meta:
        unique_together = ('cod_producto', 'insumo')

    def __str__(self):
        return f"{self.cod_producto} - {self.insumo} ({self.cantidad} {self.unidad_medida})"
    def __str__(self):
        return f"{self.cod_producto} - {self.insumo} ({self.cantidad} {self.unidad_medida})"

class RecetaPersonalizacion(models.Model):
    TIPO_CHOICES = [
        ('MASA', 'Masa'),
        ('GLASEADO', 'Glaseado'),
        ('TOPPING', 'Topping'),
    ]

    cod_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas_personalizadas')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    unidad_medida = models.CharField(max_length=10, default='g')  # o 'cucharada' si es masa

    class Meta:
        unique_together = ('cod_producto', 'tipo', 'insumo')

    def cantidad_base(self):
        if self.tipo == 'MASA':
            return 15  # cucharada
        elif self.tipo == 'GLASEADO':
            return 200  # gramos
        elif self.tipo == 'TOPPING':
            return 100  # gramos
        return 0

    def cantidad_total(self):
        multiplicador = self.cod_producto.get_multiplicador()
        return self.cantidad_base() * multiplicador

    def __str__(self):
        return f"{self.cod_producto} - {self.tipo} - {self.insumo} ({self.cantidad_base()}{self.unidad_medida})"

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"Notificación para {self.usuario.email}: {self.mensaje[:30]}"
