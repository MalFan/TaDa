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
from views import get_form_context

# Create your views here.
def home(request):
	context = {}
	context.update(get_form_context())
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
			'1791528', # Upcoming 1
			'1528100',
			'2784678',
			'2298394',
			]
	id_list2 = [
			'2310332', # Upcoming 2
			'1823664',
			'2692250',
			'2039393',
			'2473794',
			'2437548',
			]
	id_list3 = [
			'2180411', # Upcoming 3
			'1809398',
			'2788710',
			'2179136',
			'1126590',
			'2737050',
			'2790236',
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
			'1951265', # In theater
			'0816692', 
			'2015381', 
			'2170439',
			'2096672',
			'2245084',
			'2980516',
			'2713180', 
			'2267998', 
			'1911658',
			]
	for m_id in id_list:
		try:
			m = Movie.objects.get(imdb_id = m_id)
			movies.append(m)
		except Movie.DoesNotExist:
			pass

	return movies


def recommend_movie(request):
	context = {}
	context.update(get_form_context())
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

def get_advanced_recommend_movies(current_user):
	if not current_user.username:
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
	context.update(get_form_context())
	context['next'] = '/'
	context['user_combos'] = get_advanced_recommend_users(request.user)
	context['request'] = request
	return render(request, 'recommend_user.html', context)

def get_recommend_users():
	users = []
	users = User.objects.all()[:20]

	return users

def get_advanced_recommend_users(u):
	if not u.username:
		return get_recommend_users()
		
	u_other = User.objects.all().exclude(username=u.username).exclude(username__in = u.profile.users_followed.all().values_list('username', flat=True))

	u_recom_list = []
	u_recom_dict = {}
	u_array = np.fromstring(u.profile.user_vector, dtype=int, sep=',')

	for u2 in u_other:
		u2_array = np.fromstring(u2.profile.user_vector, dtype=int, sep=',')
		dist = np.linalg.norm(u_array - u2_array)
		similarity = 1 / ( 1 + dist )
		if not u2.username in u_recom_dict:
			u_recom_list.append((u2, similarity))
			u_recom_dict[u2.username] = similarity
		elif similarity > u_recom_dict[u2.username]:
			u_recom_list = update_in_alist(u_recom_list, u2, similarity)
			u_recom_dict[u2.username] = similarity

	sorted_u_recom = sorted(u_recom_list, key=itemgetter(1))[::-1]
	users = [u_tuple[0] for u_tuple in sorted_u_recom[:20]]

	return users