from django import forms
from .models import Usuario  # tu modelo

class UsuarioForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar clave")

    class Meta:
        model = Usuario
        fields = ['nomUsua', 'apellUsua', 'emailUsua', 'passwUsua']
        widgets = {
            'passwUsua': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("passwUsua")
        pass2 = cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            self.add_error("password2", "Las contraseñas no coinciden")
