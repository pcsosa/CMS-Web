from django import forms
from .models_cont import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'email', 'comentario']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario...'}),
        }
