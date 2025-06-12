from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Cliente,  Venta

class RegistroUsuarioForm(UserCreationForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''

    class Meta:
        model = Usuario
        fields = ['email', 'nom_usua', 'apell_usua', 'tele_usua']
        labels = {
            'email': 'Correo Electrónico',
            'nom_usua': 'Nombre',
            'apell_usua': 'Apellido',
            'tele_usua': 'Teléfono',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control shadow'}),
            'nom_usua': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control shadow'}),
            'apell_usua': forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control shadow'}),
            'tele_usua': forms.TextInput(attrs={'placeholder': 'Teléfono', 'class': 'form-control shadow'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class UsuarioForm(UserCreationForm):
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''  # Esto elimina todas las etiquetas

    class Meta:
        model = Usuario
        fields = ['email', 'nom_usua', 'apell_usua', 'tele_usua', 'rol']
        labels = {
            'email': 'Correo Electrónico',
            'nom_usua': 'Nombre',
            'apell_usua': 'Apellido',
            'tele_usua': 'Teléfono',
            'rol': 'Rol',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control shadow'}),
            'nom_usua': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control shadow'}),
            'apell_usua': forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control shadow'}),
            'tele_usua': forms.TextInput(attrs={'placeholder': 'Teléfono', 'class': 'form-control shadow'}),
            'rol': forms.Select(attrs={'class': 'form-control shadow'}, choices=Usuario.ROLES),
        }

    def clean(self):
        cleaned_data = super().clean()
        # La validación de contraseñas ya la hace UserCreationForm automáticamente
        return cleaned_data
    
    
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

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        exclude = ['subtotal', 'iva', 'total']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['cod_producto', 'cantidad', 'precio_unitario', 'fecha_entrega']
        widgets = {
            'fecha_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CombinacionProductoForm(forms.ModelForm):
    class Meta:
        model = CombinacionProducto
        fields = [
            'cod_producto', 
            'cod_sabor_masa_1', 
            'cod_glaseado_1', 
            'cod_topping_1'
        ]
        widgets = {
            'cod_producto': forms.Select(attrs={'class': 'form-control'}),
            'cod_sabor_masa_1': forms.Select(attrs={'class': 'form-control'}),
            'cod_glaseado_1': forms.Select(attrs={'class': 'form-control'}),
            'cod_topping_1': forms.Select(attrs={'class': 'form-control'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        exclude = ['cod_venta', 'estado_pago', 'transaccion_id']

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
        fields = ['cod_insumo', 'cnt_entrada', 'precio_entrada', 'fecha_caducidad', 'lote']


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
            'firma_recepcion',
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
            'firma_recepcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre o firma de quien recibe'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'cod_domi': forms.Select(attrs={'class': 'form-select'}),
            'tarifa_envio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


#Envios  del administrador
from .models import Envio

from django import forms
from .models import Envio

