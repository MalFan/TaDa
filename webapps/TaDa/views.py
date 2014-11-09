from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth.views import logout, login
from django.contrib.auth.decorators import login_required

import imdb

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
	return render(request, 'home.html', context)

def recommend_movie(request):
	context = {}
	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['search_form'] = SearchForm() 
	
	context['next_page'] = '/recommend-movie'
	return render(request, 'recommend_movie.html', context)

def search(request):
	context = {}
	context['search_form'] = SearchForm(request.GET) 
	keywords = request.GET['search_content']
	search_type = request.GET['search_type']
	if search_type == 'all':
		movies = Movie.objects.filter(title__contains = keywords)
		names = Person.objects.filter(name__contains = keywords, has_full_info = True)

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

		context['name_combos'] = names

	elif search_type == 'movies':
		movies = Movie.objects.filter(title__contains = keywords)
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
	elif search_type == 'names':
		names = Person.objects.filter(name__contains = keywords, has_full_info = True)
		context['name_combos'] = names

	return render(request, 'search.html', context)

def movie(request):
	context = {}
	return render(request, 'movie.html', context)


def register(request):
	context = {}
	regis_form = RegistrationForm(request.POST)
	context['regis_form'] = regis_form
	context['search_form'] = SearchForm() 

	if request.method == 'GET':
		return redirect('/')

	if not regis_form.is_valid():
		return redirect('/')

	new_user = User.objects.create_user(username=regis_form.cleaned_data['username'],
										email=regis_form.cleaned_data['email'],
										password=regis_form.cleaned_data['password1'])
	new_user.save()
	new_user = authenticate(username=regis_form.cleaned_data['username'],
										email=regis_form.cleaned_data['email'],
										password=regis_form.cleaned_data['password1'])
	
	auto_login(request, new_user)
	return redirect('/')

def log_in(request):
	# # next = next_page

	# login_form = LoginForm(request.POST)

	# if not login_form.is_valid():
	# 	print 22
	# 	return redirect('/')
	# # context['login_form'] = login_form

	# new_user = authenticate(username=login_form.cleaned_data['username'],
	# 									password=login_form.cleaned_data['password'])
	# login(request, new_user)

	# next = ''
	# if not 'next1' in request.POST:
	# 	return redirect('/')
	# else:
	# 	next = request.POST['next1']

	# return redirect(next)
	# next = request.POST['next1']

	if request.method == 'GET':
		return redirect('/')

	return login(request,redirect_field_name='/',
							template_name='home.html',
							authentication_form=LoginForm,
							extra_context={'login_form':LoginForm,'regis_form':RegistrationForm})

@login_required
def log_out(request):
	# next = next_page
	return logout(request,next_page='/')