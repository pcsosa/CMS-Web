from .models import Comentario
from django import formsclass

 CommentForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('usuario', 'email', 'comentario')