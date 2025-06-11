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
    
from django import forms
from .models import Venta, DetalleVenta, Pago
from django.forms import inlineformset_factory

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cod_cliente', 'subtotal', 'iva', 'total', 'estado', 'direccion_entrega', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'direccion_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'cod_cliente': forms.Select(attrs={'class': 'form-select'}),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['cod_producto', 'cantidad', 'precio_unitario', 'fecha_entrega']
        widgets = {
            'cod_producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_entrega': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

DetalleVentaFormSet = inlineformset_factory(
    Venta, DetalleVenta,
    form=DetalleVentaForm,
    extra=1,
    can_delete=False
)

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago', 'monto_total', 'estado_pago', 'transaccion_id']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'estado_pago': forms.Select(attrs={'class': 'form-select'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'transaccion_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
