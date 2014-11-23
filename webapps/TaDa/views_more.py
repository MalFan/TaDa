from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth.views import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.utils import timezone 

import imdb
import collections
from operator import itemgetter

from models import *
from forms import *
from views import *

# Create your views here.
def cast_list(request,movie_id):
	context = {}
	context['search_form'] = SearchForm()	
	context['review_form'] = ReviewForm()
	context['regis_form'] = RegistrationForm()
	context['login_form'] = LoginForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)
	movie_combo = {
			'imdb_id' : m.imdb_id,
			'title' : m.title,
			'year' : m.year,
			'duration' : m.duration,
			'cover' : m.cover,
			'director_list' : m.director_list.all(),
			'writer_list' : m.writer_list.all(),
			'cast_character_list' : zip(m.cast_list.all(), m.character_list.all()),
			'storyline' : m.short_storyline,
			'genre_list' : m.genre_list.all(),
			'certificate' : m.certificate}
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	
	return render(request, 'cast_list.html', context)


def review_list(request,movie_id):
	context = {}
	context['search_form'] = SearchForm()	
	context['review_form'] = ReviewForm()
	context['regis_form'] = RegistrationForm()
	context['login_form'] = LoginForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)
	movie_combo = {
			'imdb_id' : m.imdb_id,
			'title' : m.title,
			'year' : m.year,
			'duration' : m.duration,
			'cover' : m.cover,
			'director_list' : m.director_list.all(),
			'writer_list' : m.writer_list.all(),
			'storyline' : m.short_storyline,
			'genre_list' : m.genre_list.all(),
			'certificate' : m.certificate}
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()

	context['reviews'] = Review.objects.filter(movie = m).order_by('id').reverse()

	return render(request, 'review_list.html', context)

def people_also_liked_list(request, movie_id):
	context = {}
	context['search_form'] = SearchForm()	
	context['review_form'] = ReviewForm()
	context['regis_form'] = RegistrationForm()
	context['login_form'] = LoginForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)
	movie_combo = {
			'imdb_id' : m.imdb_id,
			'title' : m.title,
			'year' : m.year,
			'duration' : m.duration,
			'cover' : m.cover,
			'director_list' : m.director_list.all(),
			'writer_list' : m.writer_list.all(),
			'storyline' : m.short_storyline,
			'genre_list' : m.genre_list.all(),
			'certificate' : m.certificate}
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['m_also'] = get_people_also_liked_movies(movie_id, request.user)
	
	return render(request, 'people_also_liked_list.html', context)

def people_who_liked_list(request,movie_id):
	context = {}
	context['search_form'] = SearchForm()	
	context['review_form'] = ReviewForm()
	context['regis_form'] = RegistrationForm()
	context['login_form'] = LoginForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)
	movie_combo = {
			'imdb_id' : m.imdb_id,
			'title' : m.title,
			'year' : m.year,
			'duration' : m.duration,
			'cover' : m.cover,
			'director_list' : m.director_list.all(),
			'writer_list' : m.writer_list.all(),
			'storyline' : m.short_storyline,
			'genre_list' : m.genre_list.all(),
			'certificate' : m.certificate}
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['u_like'] = get_people_who_liked_this(movie_id, request.user)
	
	return render(request, 'people_who_liked_list.html', context)