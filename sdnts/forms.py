from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Cliente,  Venta
from django.core.validators import RegexValidator

# Validador: solo letras (con tildes, ñ, ü) y espacios
solo_letras = RegexValidator(
    r'^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$',
    'Solo se permiten letras y espacios en los campos nombre/apellido.'
)

class RegistroUsuarioForm(UserCreationForm):
    # Campos de autenticación -----------------------------
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control shadow'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Contraseña',
            'class': 'form-control shadow'
        })
    )

    # Campos de tu modelo ---------------------------------
    nom_usua = forms.CharField(
        label='Nombre',
        validators=[solo_letras],
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'form-control shadow'
        })
    )
    apell_usua = forms.CharField(
        label='Apellido',
        validators=[solo_letras],
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'form-control shadow'
        })
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo Electrónico',
            'class': 'form-control shadow'
        })
    )
    tele_usua = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'placeholder': 'Teléfono',
            'class': 'form-control shadow'
        })
    )

    # Meta y ajustes --------------------------------------
    class Meta:
        model = Usuario
        fields = ['nom_usua', 'apell_usua', 'email', 'tele_usua']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ocultamos labels en el HTML (ya están en los placeholders)
        for field in self.fields.values():
            field.label = ''
            
            

class UsuarioForm(UserCreationForm):
    # Campos de autenticación (los de UserCreationForm + estilos) ───────────────
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control shadow'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Contraseña',
            'class': 'form-control shadow'
        })
    )

    # Campos con validación extra ───────────────────────────────────────────────
    nom_usua = forms.CharField(
        label='Nombre',
        validators=[solo_letras],
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'form-control shadow'
        })
    )
    apell_usua = forms.CharField(
        label='Apellido',
        validators=[solo_letras],
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'form-control shadow'
        })
    )

    # Meta y resto de widgets ───────────────────────────────────────────────────
    class Meta:
        model = Usuario
        fields = ['email', 'nom_usua', 'apell_usua', 'tele_usua', 'rol']
        labels = {
            'email': 'Correo Electrónico',
            'tele_usua': 'Teléfono',
            'rol': 'Rol',
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Correo Electrónico',
                'class': 'form-control shadow'
            }),
            'tele_usua': forms.TextInput(attrs={
                'placeholder': 'Teléfono',
                'class': 'form-control shadow'
            }),
            'rol': forms.Select(attrs={
                'class': 'form-control shadow'
            }, choices=Usuario.ROLES),
        }

    # Oculta las etiquetas en el HTML (ya están en los placeholders)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
    
class CargarDatosForm(forms.Form):
    TIPOS_ARCHIVO = (
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
    )
    
    tipo_archivo = forms.ChoiceField(
        choices=TIPOS_ARCHIVO,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.json'
        })
    )
    
    descripcion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción opcional del archivo...'
        })
    )
    
class PerfilAdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nom_usua', 'apell_usua', 'tele_usua']
        widgets = {
            'nom_usua': forms.TextInput(attrs={'class': 'form-control'}),
            'apell_usua': forms.TextInput(attrs={'class': 'form-control'}),
            'tele_usua': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
from django.contrib.auth.forms import PasswordChangeForm

class CambiarContrasenaForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
# ventas
from django import forms
from .models import Venta, DetalleVenta, Pago, CombinacionProducto
from datetime import date, timedelta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        exclude = ['subtotal', 'iva', 'total']

    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        fecha_minima = date.today() + timedelta(days=3)
        if fecha_entrega and fecha_entrega < fecha_minima:
            raise forms.ValidationError("La fecha de entrega debe ser al menos 3 días después de hoy.")
        return fecha_entrega
from datetime import date, timedelta

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['cod_producto', 'cantidad', 'precio_unitario', 'fecha_entrega']
        widgets = {
            'fecha_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'precio_unitario': forms.NumberInput(attrs={'readonly': 'readonly'})  # Desactiva edición manual
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fecha_minima = (date.today() + timedelta(days=3)).isoformat()
        self.fields['fecha_entrega'].widget.attrs['min'] = fecha_minima

    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        fecha_minima = date.today() + timedelta(days=3)
        if fecha_entrega and fecha_entrega.date() < fecha_minima:
            raise forms.ValidationError("La fecha de entrega debe ser al menos 3 días después de hoy.")
        return fecha_entrega

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("❌ La cantidad no puede ser cero ni negativa.")
        return cantidad

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is not None and precio < 0:
            raise forms.ValidationError("❌ El precio unitario no puede ser negativo.")
        return precio


class CombinacionProductoForm(forms.ModelForm):
    class Meta:
        model = CombinacionProducto
        fields = [
            'cod_sabor_masa_1', 
            'cod_glaseado_1', 
            'cod_topping_1'
        ]
        widgets = {
            'cod_sabor_masa_1': forms.Select(attrs={'class': 'form-control'}),
            'cod_glaseado_1': forms.Select(attrs={'class': 'form-control'}),
            'cod_topping_1': forms.Select(attrs={'class': 'form-control'}),
        }

from django.forms import modelformset_factory
from .models import DetalleVenta, CombinacionProducto    
CombinacionProductoFormSet = modelformset_factory(
    CombinacionProducto,
    form=CombinacionProductoForm,
    extra=1,
    can_delete=True
)
DetalleVentaFormSet = modelformset_factory(
    DetalleVenta,
    form=DetalleVentaForm,
    extra=1,
    can_delete=True
)


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        exclude = ['cod_venta', 'estado_pago', 'transaccion_id']

    def clean_valor_pagado(self):
        valor = self.cleaned_data.get('valor_pagado')
        if valor is not None and valor < 0:
            raise forms.ValidationError("El valor pagado no puede ser negativo.")
        return valor
#produccion
from .models import Produccion, Salida, Entrada, Envio

class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ['cod_venta', 'observaciones']

class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        fields = ['cod_insumo', 'cantidad']

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['cod_insumo', 'cod_proveedor', 'cnt_entrada', 'precio_entrada', 'fecha_caducidad']
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_cnt_entrada(self):
        cnt = self.cleaned_data.get('cnt_entrada')
        if cnt is not None and cnt < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cnt

    def clean_precio_entrada(self):
        precio = self.cleaned_data.get('precio_entrada')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
    
    
    
class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = [
            'cod_domi',
            'fecha_asignacion',
            'fecha_salida',
            'fecha_entrega',
            'estado',
            'tarifa_envio',
            'observaciones',
        ]
        widgets = {
            'fecha_asignacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_salida': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_entrega': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
            
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'cod_domi': forms.Select(attrs={'class': 'form-select'}),
            'tarifa_envio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

from django import forms
from .models import Envio

class EnvioDomiciliarioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ['fecha_entrega', 'segunda_fecha', 'estado', 'observaciones']
        widgets = {
            'fecha_entrega': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'segunda_fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe observaciones aquí...'
            }),
        }

#proveedores
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nom_proveedor', 'telefono_proveedor', 'direccion_proveedor', 'email_proveedor', 'novedad_proveedor']
        widgets = {
            'nom_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'email_proveedor': forms.EmailInput(attrs={'class': 'form-control'}),
            'novedad_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
        }

#entradas

from .models import Entrada

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['cod_insumo', 'cod_proveedor', 'cnt_entrada', 'precio_entrada', 'fecha_caducidad']
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from .models import Insumo

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['cod_categoria', 'nomb_insumo', 'cnt_insumo', 'unidad_medida']
        widgets = {
            'cod_categoria': forms.Select(attrs={'class': 'form-control'}),
            'nomb_insumo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del insumo'}),
            'cnt_insumo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
        }

    def clean_nomb_insumo(self):
     nombre = self.cleaned_data['nomb_insumo'].strip()
     if nombre.isdigit():
        raise forms.ValidationError("El nombre del insumo no puede ser solo números.")
        qs = Insumo.objects.filter(nomb_insumo__iexact=nombre)
     if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
     if qs.exists():
        raise forms.ValidationError("Ya existe un insumo con ese nombre.")
     return nombre
    
    
    
from django import forms
from .models import Salida

class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        fields = ['cod_produccion', 'cod_insumo', 'cantidad']
        widgets = {
            'cod_produccion': forms.Select(attrs={'class': 'form-control'}),
            'cod_insumo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
from django import forms
from .models import RecetaProducto
from django.forms import modelformset_factory

# Definir insumos básicos por nombre (puedes usar ID si prefieres)
INSUMOS_BASICOS = [
    'Huevos',
    'Azúcar',
    'Sal',
    'Mantequilla',
    'Leche',
    'Harina de trigo',
    'Polvo para hornear',
]

class RecetaProductoForm(forms.ModelForm):
    class Meta:
        model = RecetaProducto
        fields = ['cantidad', 'unidad_medida']


RecetaProductoFormSet = modelformset_factory(
    RecetaProducto,
    fields=('insumo', 'cantidad', 'unidad_medida'),
    extra=1,
    can_delete=True
)
from django import forms
from .models import RecetaPersonalizacion

class RecetaPersonalizacionForm(forms.ModelForm):
    class Meta:
        model = RecetaPersonalizacion
        fields = ['tipo', 'insumo', 'unidad_medida']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
        }

RecetaPersonalizacionFormSet = forms.modelformset_factory(
    RecetaPersonalizacion,
    form=RecetaPersonalizacionForm,
    extra=3,  #  más combinaciones
    can_delete=True
)


