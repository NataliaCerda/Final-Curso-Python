from mailbox import NoSuchMailboxError
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.
class Profesor(models.Model):
    nombre = models.CharField("Nombre" ,max_length=30) # Texto
    apellido = models.CharField("Apellido" ,max_length=30) # Texto
    email = models.EmailField("email" ,blank=True, null=True) # Email - Opcional
    profesion = models.CharField("Profesion" ,max_length=30)
    
    class Meta:
        verbose_name_plural = "Profesores"

class Curso(models.Model):
    nombre = models.CharField("Nombre" ,max_length=30) # Texto
    comision = models.IntegerField("Comisión")
    descripcion = models.TextField("Descripcion Curso", null=True, blank=True)
    imagen = models.ImageField(upload_to='curso/', blank=True, null=True)

class Estudiante(models.Model):
    nombre = models.CharField("Nombre" ,max_length=30) # Texto
    apellido = models.CharField("Apellido" ,max_length=30) # Texto
    email = models.EmailField("email" ,blank=True, null=True) # Email - Opcional

class Avatar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Si elimino un usuario se elimina la imagen
    imagen = models.ImageField(upload_to='avatar/', blank=True, null=True)

class Comentario(models.Model):
    curso = models.ForeignKey(Curso, related_name='comentario',on_delete=models.CASCADE )
    autor = models.CharField(max_length=200)
    texto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.texto