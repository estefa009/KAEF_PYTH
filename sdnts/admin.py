from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Administrador, Cliente, Domiciliario,
    Proveedor, CategoriaInsumo, Insumo, Entrada,
    Producto, Venta, DetalleVenta, Pago,
    Produccion, Salida, Envio, SaborMasa,
    Glaseado, Topping, CombinacionProducto
)

# 1. Configuración personalizada para el Usuario
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nom_usua', 'apell_usua', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    search_fields = ('email', 'nom_usua', 'apell_usua')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nom_usua', 'apell_usua', 'tele_usua')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom_usua', 'apell_usua', 'tele_usua', 'rol', 'password1', 'password2'),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)

# 2. Configuración para modelos relacionados con usuarios
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('cod_admin', 'cod_usua', 'estado_admin')
    list_filter = ('estado_admin',)
    raw_id_fields = ('cod_usua',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cod_cliente', 'cod_usua', 'direc_cliente', 'historial_compras')
    search_fields = ('cod_usua__nom_usua', 'direc_cliente')
    raw_id_fields = ('cod_usua',)

@admin.register(Domiciliario)
class DomiciliarioAdmin(admin.ModelAdmin):
    list_display = ('cod_domi', 'cod_usua', 'disponibilidad')
    list_filter = ('disponibilidad',)
    raw_id_fields = ('cod_usua',)

# 3. Configuración para inventario y productos
class EntradaInline(admin.TabularInline):
    model = Entrada
    extra = 1
    fields = ('nom_entrada', 'cnt_entrada', 'precio_entrada', 'fecha_caducidad')

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nomb_insumo', 'cod_categoria', 'cnt_insumo', 'unidad_medida')
    list_filter = ('cod_categoria',)
    search_fields = ('nomb_insumo',)
    inlines = [EntradaInline]

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nomb_pro', 'tamano', 'capacidad', 'prec_pro', 'activo')
    list_filter = ('tamano', 'activo')
    search_fields = ('nomb_pro',)
    list_editable = ('activo',)

# 4. Configuración para ventas y producción
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ('subtotal',)

class CombinacionProductoInline(admin.TabularInline):
    model = CombinacionProducto
    extra = 1
    fields = ('cod_producto', 'cod_sabor_masa_1', 'cod_sabor_masa_2', 
              'cod_glaseado_1', 'cod_glaseado_2', 
              'cod_topping_1', 'cod_topping_2')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cod_venta', 'cliente_info', 'fecha_hora', 'total', 'estado')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('cod_cliente__cod_usua__nom_usua',)
    inlines = [DetalleVentaInline, CombinacionProductoInline]
    readonly_fields = ('subtotal', 'iva', 'total')
    
    def cliente_info(self, obj):
        return f"{obj.cod_cliente.cod_usua.nom_usua} {obj.cod_cliente.cod_usua.apell_usua}"
    cliente_info.short_description = 'Cliente'

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('cod_pago', 'cod_venta', 'metodo_pago', 'monto_total', 'estado_pago')
    list_filter = ('metodo_pago', 'estado_pago')
    search_fields = ('cod_venta__cod_venta',)

# 5. Configuración para producción y envíos
class SalidaInline(admin.TabularInline):
    model = Salida
    extra = 1

@admin.register(Produccion)
class ProduccionAdmin(admin.ModelAdmin):
    list_display = ('cod_produccion', 'cod_venta', 'estado', 'fecha_inicio', 'fecha_fin')
    list_filter = ('estado',)
    inlines = [SalidaInline]

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ('cod_envio', 'cod_venta', 'domiciliario_info', 'estado', 'fecha_asignacion')
    list_filter = ('estado',)
    
    def domiciliario_info(self, obj):
        if obj.cod_domi:
            return f"{obj.cod_domi.cod_usua.nom_usua} {obj.cod_domi.cod_usua.apell_usua}"
        return "No asignado"
    domiciliario_info.short_description = 'Domiciliario'

# 6. Configuración para sabores y toppings
@admin.register(SaborMasa)
class SaborMasaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Glaseado)
class GlaseadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'color', 'descripcion')
    list_filter = ('tipo', 'color')
    search_fields = ('nombre',)

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# 7. Modelos adicionales
admin.site.register([Proveedor, CategoriaInsumo])