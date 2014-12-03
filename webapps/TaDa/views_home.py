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
from django.db import transaction

import imdb
import numpy as np
import collections
from operator import itemgetter

from models import *
from forms import *

# Create your views here.
def home(request):
	context = {}
	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['search_form'] = SearchForm() 
	context['next'] = '/'
	context['movie_combos'] = get_in_theater_movies()
	context['request'] = request
	context['email_from'] = EmailEnterForm()
	context.update(get_upcoming_movies())
	return render(request, 'home.html', context)

def get_upcoming_movies():
	context = {}
	movies1 = []
	movies2 = []
	movies3 = []
	context['upcoming_movies_combo1'] = []
	context['upcoming_movies_combo2'] = []
	context['upcoming_movies_combo3'] = []

	id_list1 = [
			'1951265',
			'3704538',
			'2171902',
			'2960930'
			]
	id_list2 = [
			'2170439',
			'1911658',
			'2084970'
			]
	id_list3 = [
			'2799166',
			'2305051',
			'2369205'
			]

	for m_id in id_list1:
		m = Movie.objects.filter(imdb_id = m_id)
		if( len(m) > 0 ):
			movies1.append(m[0])	
	for m_id in id_list2:
		m = Movie.objects.filter(imdb_id = m_id)
		if( len(m) > 0 ):
			movies2.append(m[0])

	for m_id in id_list3:
		m = Movie.objects.filter(imdb_id = m_id)
		if( len(m) > 0 ):
			movies3.append(m[0])

	context['upcoming_movies_combo1'] = movies1		
	context['upcoming_movies_combo2'] = movies2
	context['upcoming_movies_combo3'] = movies3
	return context

def get_in_theater_movies():
	movies = []
	id_list = [
			'0829150', 
			'0455944', 
			'2713180', 
			'2267998', 
			'2911666', 
			'1790864', 
			'2872718', 
			'0816692', 
			'1872194', 
			'2262227',
			'1100089',
			'3125324',
			'2096672',
			'2398231']
	for m_id in id_list:
		try:
			m = get_object_or_404(Movie, imdb_id = m_id)
			movies.append(m)
		except Movie.DoesNotExist:
			pass

	return movies


def recommend_movie(request):
	context = {}
	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['search_form'] = SearchForm() 
	context['movie_combos'] = get_advanced_recommend_movies(request.user)
	context['next_page'] = '/recommend-movie'
	context['request'] = request
	return render(request, 'recommend_movie.html', context)
	
def get_recommend_movies():
	movies = []
	movies = Movie.objects.all().annotate(num_likes=Count('like_list')).order_by('num_likes').reverse()[:15]

	return movies

# http://stackoverflow.com/questions/8559217/python-update-a-value-in-a-list-of-tuples
def update_in_alist(alist, key, value):
    	return [(k,v) if (k != key) else (key, value) for (k, v) in alist]

def get_advanced_recommend_movies(urrent_user):
	if not urrent_user.username:
		return get_recommend_movies()
		
	m_liked = current_user.m_like.all()
	m_disliked = current_user.m_dislike.all()

	if not m_liked:
		return get_recommend_movies()
	m_other = Movie.objects.exclude(like_list__in=[current_user]). \
							exclude(dislike_list__in=[current_user])

	m_recom_list = []
	m_recom_dict = {}
	for m in m_liked:
		m_array = np.fromstring(m.vector, dtype=int, sep=',')
		for m2 in m_other:
			m2_array = np.fromstring(m2.vector, dtype=int, sep=',')
			dist = np.linalg.norm(m_array - m2_array)
			similarity = 1 / ( 1 + dist )
			if not m2.imdb_id in m_recom_dict:
				m_recom_list.append((m2, similarity))
				m_recom_dict[m2.imdb_id] = similarity
			elif similarity > m_recom_dict[m2.imdb_id]:
				m_recom_list = update_in_alist(m_recom_list, m2, similarity)
				m_recom_dict[m2.imdb_id] = similarity

	sorted_m_recom = sorted(m_recom_list, key=itemgetter(1))[::-1]

	movie_combos = []
	for m_tuple in sorted_m_recom[:15]:
		m = m_tuple[0]
		movie_combo = {'imdb_id' : m.imdb_id,
						'title' : m.title,
						'year' : m.year,
						'duration' : m.duration,
						'cover' : m.cover,
						'director_list' : m.director_list.all(),
						'cast_list' : m.cast_list.all()[:4],
						'storyline' : m.short_storyline,
						'genre_list' : m.genre_list.all(),
						'certificate' : m.certificate,
						'ticket_url' : m.ticket_url}
		movie_combos.append(movie_combo)

	return movie_combos

def recommend_user(request):
	context = {}
	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['search_form'] = SearchForm() 
	context['next'] = '/'
	context['user_combos'] = User.objects.all()[:20];
	context['request'] = request
	return render(request, 'recommend_user.html', context)