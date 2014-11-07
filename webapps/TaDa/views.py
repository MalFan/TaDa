from django.shortcuts import render
import imdb

from models import *
# from forms import *

# Create your views here.
def home(request):
	context = {}
	return render(request, 'home.html', context)

def recommend_movie(request):
	context = {}
	return render(request, 'recommend_movie.html', context)

def search(request):
	context = {}
	keyword = request.GET['keyword']
	movies = Movie.objects.filter(title__contains = keyword)
	context['movie_combos'] = []
	for m in movies:
		movie_combo = {
				'imdb_id' : m.imdb_id,
				'title' : m.title,
				'year' : m.year,
				'duration' : m.duration,
				'cover' : m.cover,
				'director_list' : m.director_list.all(),
				'writer_list' : m.writer_list.all(),
				'cast_list' : m.cast_list.all()[:15],
				'storyline' : m.short_storyline,
				'genre_list' : m.genre_list.all(),
				'certificate' : m.certificate}
		context['movie_combos'].append(movie_combo)

	return render(request, 'search.html', context)


