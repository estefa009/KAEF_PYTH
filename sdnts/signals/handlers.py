# saints/signals/handlers.py
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from sdnts.models import Entrada, Salida, Venta, Pago, Envio, CombinacionProducto,Usuario,Cliente,Domiciliario, Administrador


@receiver(post_save, sender=Usuario)
def crear_modelo_por_rol(sender, instance, created, **kwargs):
    if created:
        if instance.rol == 'DOMI':
            Domiciliario.objects.create(cod_usua=instance)
        elif instance.rol == 'CLIENTE':
            Cliente.objects.create(cod_usua=instance, direc_cliente='Sin dirección')
        elif instance.rol == 'ADMIN':
            Administrador.objects.create(cod_usua=instance, estado_admin='ACTIVO')

# Trigger 1: Actualizar inventario después de entrada
@receiver(post_save, sender=Entrada)
def actualizar_inventario_despues_entrada(sender, instance, created, **kwargs):
    """
    Reemplaza: AFTER INSERT ON entradas
    Actualiza el stock cuando hay una nueva entrada
    """
    if created:
        insumo = instance.cod_insumo
        insumo.cnt_insumo += instance.cnt_entrada
        insumo.save()

# Trigger 2: Validar stock antes de salida
@receiver(pre_save, sender=Salida)
def validar_stock_antes_salida(sender, instance, **kwargs):
    """
    Reemplaza: BEFORE INSERT ON salida
    Valida que haya suficiente stock
    """
    if instance.cod_insumo.cnt_insumo < instance.cantidad:
        raise ValidationError("Stock insuficiente para esta salida")

# Trigger 3: Actualizar estado de venta cuando se paga
@receiver(post_save, sender=Pago)
def actualizar_estado_venta(sender, instance, created, **kwargs):
    """
    Reemplaza: AFTER UPDATE ON pago
    Cambia estado de venta cuando pago se marca como PAGADO
    """
    if instance.estado_pago == 'PAGADO':
        venta = instance.cod_venta
        venta.estado = 'PREPARACION'
        venta.save()

# Trigger 4: Crear producción automáticamente
@receiver(post_save, sender=Venta)
def crear_produccion_automatica(sender, instance, created, **kwargs):
    """
    Reemplaza: AFTER UPDATE ON venta
    Crea registro de producción cuando venta pasa a PREPARACION
    """
    if instance.estado == 'PREPARACION' and not hasattr(instance, 'produccion'):
        from sdnts.models import Produccion
        Produccion.objects.create(cod_venta=instance)

# Trigger 5: Validar combinaciones de productos
@receiver(pre_save, sender=CombinacionProducto)
def validar_combinacion_producto(sender, instance, **kwargs):
    """
    Reemplaza: BEFORE INSERT ON combinacion_producto
    Valida reglas de combinaciones según tamaño
    """
    producto = instance.cod_producto
    # Elimina validaciones de campos eliminados
    # Si necesitas reglas por tamaño, actualízalas aquí según los campos actuales
    pass