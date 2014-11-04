from django.shortcuts import render
from django.core import serializers
import imdb

from models import *
# from forms import *

# Create your views here.
def admin_homepage(request):
	context = {}
	# i = imdb.IMDb()
	# movie_list = i.get_top250_movies()
	# context['movie_list'] = movie_list
	return render(request, 'admin_homepage.html', context)

def admin_search(request):
	context = {}
	i = imdb.IMDb()
	movie_list = i.search_movie(request.GET['search'])

	context['movie_list'] = movie_list

	return render(request, 'admin_homepage.html', context)

def admin_add_movie(request, movie_id):
	context = {}
	i = imdb.IMDb()
	movie = i.get_movie(movie_id)

	imdbid = movie_id
	title = movie['title']
	year = movie['year']
	cover = movie['cover url'] # add a if condition 
	director = movie['director']
	writer = movie['writer']
	cast = movie['cast']
	storyline = movie['plot'][0]
	genres = movie['genres']
	certificates = movie['certificates']
	# m = Movie(
	# 		title = movie.title,
	# 		year = movie.year,
	# 		storyline = movie.plot)
	# m.save()
	# context['movie'] = movie
	context['imdbid'] = imdbid
	context['title'] = title
	context['year'] = year
	context['cover'] = cover
	context['director'] = director
	context['writer'] = writer
	context['cast'] = cast[:15]
	context['storyline'] = storyline
	context['genres'] = genres
	context['certificate'] = [cer for cer in certificates if 'USA' in cer]

	return render(request, 'admin_movie.html', context)
