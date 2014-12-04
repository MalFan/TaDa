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
import collections
from operator import itemgetter

from models import *
from forms import *
from views import *

max_id = 9223372036854775807
# Create your views here.
def movie_cast_list(request,movie_id):
	context = {}
	context.update(get_form_context())
	context['review_form'] = ReviewForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)
	review_form = ReviewForm()
	context['m'] = m
	context['m_cast_character_list'] = zip(m.cast_list.all(), m.character_list.all())
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['request'] = request
	return render(request, 'movie_cast_list.html', context)


def movie_review_list(request,movie_id):
	context = {}
	context.update(get_form_context())
	context['review_form'] = ReviewForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)

	review_form = ReviewForm()
	context['m'] = m
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()

	context['reviews'] = Review.objects.filter(movie = m).order_by('id').reverse()
	context['request'] = request
	return render(request, 'movie_review_list.html', context)

def movie_people_also_liked_list(request, movie_id):
	context = {}
	context.update(get_form_context())
	context['review_form'] = ReviewForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)

	review_form = ReviewForm()
	context['m'] = m
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['m_also'] = get_people_also_liked_movies(movie_id, request.user)
	context['request'] = request
	return render(request, 'movie_people_also_liked_list.html', context)

def movie_people_who_liked_list(request,movie_id):
	context = {}
	context.update(get_form_context())
	context['review_form'] = ReviewForm()

	m = get_object_or_404(Movie, imdb_id = movie_id)

	review_form = ReviewForm()
	context['m'] = m
	context['like_num'] = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['u_like'] = get_people_who_liked_this(movie_id, request.user)
	context['request'] = request
	return render(request, 'movie_people_who_liked_list.html', context)

def profile_movie_list(request, view_user_id):
	if int(view_user_id) > max_id:
		raise Http404
	context = {}
	context.update(get_form_context())
	context['request'] = request
	context['user'] = request.user
	user_be_view = get_object_or_404(User,id = view_user_id)

	if request.user == user_be_view:
		context['view_user'] = request.user
		profile = get_object_or_404(Profile, user = user_be_view)
		intro_form = IntroForm(instance = profile)
		photo_form = PhotoForm(instance = profile)
		context['intro_form'] = intro_form
		context['photo_form'] = photo_form
	else:
		context['view_user'] = user_be_view

	context['reviews'] = Review.objects.filter(publisher = user_be_view).order_by('id').reverse()
	
	if Profile.objects.filter(user = user_be_view).count() > 0:
		profile = get_object_or_404(Profile, user = user_be_view)
		context['profile'] = profile
	
	context['search_form'] = SearchForm()
	user_be_followed = get_object_or_404(User, id = view_user_id)
	if request.user.username:
		profile_of_login_user = get_object_or_404(Profile, user = request.user)
		if user_be_followed in profile_of_login_user.users_followed.all():
			context['follow_text'] = 'unfollow'
		else:
			context['follow_text'] = 'follow'
	else:
		context['follow_text'] = 'follow'
	return render(request, 'profile_movie_list.html', context)

def profile_review_list(request, view_user_id):
	if int(view_user_id) > max_id:
		raise Http404
	context = {}
	context.update(get_form_context())
	context['request'] = request
	context['user'] = request.user
	user_be_view = get_object_or_404(User,id = view_user_id)

	if request.user == user_be_view:
		context['view_user'] = request.user
		profile = get_object_or_404(Profile, user = user_be_view)
		intro_form = IntroForm(instance = profile)
		photo_form = PhotoForm(instance = profile)
		context['intro_form'] = intro_form
		context['photo_form'] = photo_form
	else:
		context['view_user'] = user_be_view

	context['reviews'] = Review.objects.filter(publisher = user_be_view).order_by('id').reverse()
	
	if Profile.objects.filter(user = user_be_view).count() > 0:
		profile = get_object_or_404(Profile, user = user_be_view)
		context['profile'] = profile
		
	context['search_form'] = SearchForm()
	user_be_followed = get_object_or_404(User, id = view_user_id)
	if request.user.username:
		profile_of_login_user = get_object_or_404(Profile, user = request.user)
		if user_be_followed in profile_of_login_user.users_followed.all():
			context['follow_text'] = 'unfollow'
		else:
			context['follow_text'] = 'follow'
	else:
		context['follow_text'] = 'follow'
	return render(request, 'profile_review_list.html', context)

def profile_following_list(request, view_user_id):
	if int(view_user_id) > max_id:
		raise Http404
	context = {}
	context.update(get_form_context())
	context['request'] = request
	context['user'] = request.user
	user_be_view = get_object_or_404(User,id = view_user_id)

	if request.user == user_be_view:
		context['view_user'] = request.user
		profile = get_object_or_404(Profile, user = user_be_view)
		intro_form = IntroForm(instance = profile)
		photo_form = PhotoForm(instance = profile)
		context['intro_form'] = intro_form
		context['photo_form'] = photo_form
	else:
		context['view_user'] = user_be_view

	context['reviews'] = Review.objects.filter(publisher = user_be_view).order_by('id').reverse()
	
	if Profile.objects.filter(user = user_be_view).count() > 0:
		profile = get_object_or_404(Profile, user = user_be_view)
		context['profile'] = profile
		
	context['search_form'] = SearchForm()
	user_be_followed = get_object_or_404(User, id = view_user_id)
	if request.user.username:
		profile_of_login_user = get_object_or_404(Profile, user = request.user)
		if user_be_followed in profile_of_login_user.users_followed.all():
			context['follow_text'] = 'unfollow'
		else:
			context['follow_text'] = 'follow'
	else:
		context['follow_text'] = 'follow'
	return render(request, 'profile_following_list.html', context)