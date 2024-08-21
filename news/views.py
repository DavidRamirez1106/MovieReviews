from django.shortcuts import render
from .models import Movie, News  # Asegúrate de importar el modelo Movie
import matplotlib.pyplot as plt  # Cambié 'plit' a 'plt'
import matplotlib
import io
import urllib, base64

def news(request):
    newss = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'newss': newss})

def statistics_view(request):
    matplotlib.use('Agg')

    # Obtener todos los años de las películas
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    # Crear la gráfica de películas por año
    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, primer gráfico
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Obtener todos los géneros únicos
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    
    genre_counts = {}
    for genre in genres:
        if isinstance(genre, str) and genre:  # Verificar que genre sea una cadena
            primary_genre = genre.split(',')[0].strip()
            count = Movie.objects.filter(genre__startswith=primary_genre).count()
            genre_counts[primary_genre] = count

    # Crear la gráfica de películas por género
    plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, segundo gráfico
    plt.bar(range(len(genre_counts)), genre_counts.values(), width=bar_width, align='center')
    plt.title('Number of Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(range(len(genre_counts)), genre_counts.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})
