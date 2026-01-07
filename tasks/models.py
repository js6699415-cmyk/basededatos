from django.db import models

# Create your models here.
from django.db import models

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
class Educacion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    institucion = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

class Habilidad(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)

class Curso(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    institucion = models.CharField(max_length=150)
    fecha = models.DateField()

