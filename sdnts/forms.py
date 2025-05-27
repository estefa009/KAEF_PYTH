from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ['email', 'nom_usua', 'apell_usua', 'tele_usua', 'passw_usua', 'password2']
        labels = {
            'email': 'Correo Electrónico',
            'nom_usua': 'Nombre',
            'apell_usua': 'Apellido',
            'tele_usua': 'Teléfono',
            'passw_usua': 'Contraseña',
        }
        widgets = {
            'passw_usua': forms.PasswordInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("passw_usua")
        password2 = cleaned_data.get("password2")
        
        if password and password2 and password != password2:
            self.add_error("password2", "Las contraseñas no coinciden")
        
        return cleaned_data