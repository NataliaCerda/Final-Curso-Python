from dataclasses import fields
import email
from math import fabs
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from coder_app.models import Comentario

class NuevoCurso(forms.Form):
    nombre = forms.CharField(max_length=30,label="Curso")
    comision = forms.IntegerField(min_value=0,label="Comisión")
    descripcion = forms.CharField(label="Descripcion", widget=forms.Textarea())
    imagen = forms.ImageField(label="Imagen", required=False)

class ProfesorNuevo(forms.Form):

    nombre = forms.CharField(max_length=30,label="Nombre")
    apellido = forms.CharField(max_length=30,label="Apellido")
    email = forms.EmailField(label="Email")
    profesion = forms.CharField(max_length=30,label="Profesion")
    
class EstudianteNuevo(forms.Form):

    # id por defecto
    nombre = forms.CharField(max_length=30,label="Nombre") # Texto
    apellido = forms.CharField(max_length=30,label="Apellido") # Texto
    email = forms.EmailField(label="email") # Email - Opcional

class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellido", required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']
        
        # help_texts = {k:"" for k in fields}

class UserEditForm(forms.Form):
    
    email = forms.EmailField(label="Email")
    imagen = forms.ImageField(label="Imagen",required=False)
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellido", required=False)
    
class EditarCurso(forms.Form):
    nombre = forms.CharField(max_length=30,label="Curso")
    comision = forms.IntegerField(min_value=0,label="Comisión")
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea())
    imagen = forms.ImageField(label="Imagen",required=False)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ('autor', 'texto', 'fecha')
    