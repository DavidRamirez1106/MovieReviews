from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)  # Título de la película
    description = models.CharField(max_length=550)  # Descripción de la película
    image = models.ImageField(upload_to='movie/images/')  # Imagen de la película
    url = models.URLField(blank=True)  # URL opcional para más información
    genre = models.CharField(blank=True, max_length=250)  # Género de la película
    year = models.IntegerField(blank=True, null=True)  # Año de la película (opcional)

    def __str__(self):
        return self.title  # Retorna el título de la película como representación del objeto

