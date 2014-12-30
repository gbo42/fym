from django import forms
from django.contrib.auth.models import User
from fym.models import Trilha, Bloco, Usuario

class TrilhaForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Coloque o nome de sua historia")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Trilha
        fields = ('name',)


class BlocoForm(forms.ModelForm):
    texto = forms.CharField(max_length=240, help_text="Escreva seu pedaco da historia")

    class Meta:
        model = Bloco
        fields = ('texto',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('apelido',)