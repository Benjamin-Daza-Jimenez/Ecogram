from django import forms
from .models import Post, Comentarios

class PosteoForm(forms.ModelForm):
    title = forms.CharField(label='',max_length=100,min_length=12,widget=forms.TextInput(attrs={'id':'titulo_post','type': 'text','class': 'form-control','placeholder': 'Escriba el título...'}))
    description = forms.CharField(label = '',min_length=1000, widget=forms.Textarea(attrs={'id':'description_post','placeholder': 'Escriba la descripción...','rows':'15','cols':'155'}))

    class Meta:
        model = Post
        fields = ['title','description','image']

class ComentariosForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt flex max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '1',
            'placeholder': 'Escribe tu comentario...'
            }),
        required=True
        )

    class Meta:
        model=Comentarios
        fields=['comment']