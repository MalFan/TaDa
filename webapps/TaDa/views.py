from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth.views import logout, login
from django.contrib.auth.decorators import login_required

import imdb
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
			'1100089',
			'3125324',
			'2096672',
			'2398231']
	id_list2 = [
			'1951265',
			'3704538',
			'2171902',
			'2960930']
	id_list3 = [
			'2170439',
			'1911658',
			'2084970']

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

	for m in movies1:
		movie_combo = {'imdb_id' : m.imdb_id,
						'title' : m.title,
						'year' : m.year,
						'duration' : m.duration,
						'cover' : m.cover,
						'director_list' : m.director_list.all(),
						'cast_list' : m.cast_list.all()[:4],
						'storyline' : m.short_storyline,
						'genre_list' : m.genre_list.all(),
						'certificate' : m.certificate}
		context['upcoming_movies_combo1'].append(movie_combo)				
	for m in movies2:
		movie_combo = {'imdb_id' : m.imdb_id,
						'title' : m.title,
						'year' : m.year,
						'duration' : m.duration,
						'cover' : m.cover,
						'director_list' : m.director_list.all(),
						'cast_list' : m.cast_list.all()[:4],
						'storyline' : m.short_storyline,
						'genre_list' : m.genre_list.all(),
						'certificate' : m.certificate}
		context['upcoming_movies_combo2'].append(movie_combo)
	for m in movies3:
		movie_combo = {'imdb_id' : m.imdb_id,
						'title' : m.title,
						'year' : m.year,
						'duration' : m.duration,
						'cover' : m.cover,
						'director_list' : m.director_list.all(),
						'cast_list' : m.cast_list.all()[:4],
						'storyline' : m.short_storyline,
						'genre_list' : m.genre_list.all(),
						'certificate' : m.certificate}
		context['upcoming_movies_combo3'].append(movie_combo)
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
			'2262227']
	for m_id in id_list:
		try:
			m = Movie.objects.get(imdb_id = m_id)
			movies.append(m)
		except Movie.DoesNotExist:
			pass

	movie_combos = []
	for m in movies:
		movie_combo = {'imdb_id' : m.imdb_id,
						'title' : m.title,
						'year' : m.year,
						'duration' : m.duration,
						'cover' : m.cover,
						'director_list' : m.director_list.all(),
						'cast_list' : m.cast_list.all()[:4],
						'storyline' : m.short_storyline,
						'genre_list' : m.genre_list.all(),
						'certificate' : m.certificate}
		movie_combos.append(movie_combo)

	return movie_combos


def recommend_movie(request):
	context = {}
	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['search_form'] = SearchForm() 
	context['movie_combos'] = get_in_theater_movies()
	context['next_page'] = '/recommend-movie'
	return render(request, 'recommend_movie.html', context)

def search(request):
	context = {}
	context['search_form'] = SearchForm(request.GET) 
	keywords = request.GET['search_content']
	search_type = request.GET['search_type']
	if search_type == 'all':
		movies = Movie.objects.filter(title__contains = keywords)
		persons = Person.objects.filter(name__contains = keywords, has_full_info = True)

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

		context['person_combos'] = persons

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
		persons = Person.objects.filter(name__contains = keywords, has_full_info = True)
		context['person_combos'] = persons

	return render(request, 'search.html', context)


def movie(request, movie_id):
	context = {}
	context['search_form'] = SearchForm()
	m = get_object_or_404(Movie, imdb_id = movie_id)
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
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['review_form'] = review_form
	movie_be_reviewed = Movie.objects.get(imdb_id = movie_id)
	reviews = Review.objects.filter(movie = movie_be_reviewed).order_by('id').reverse()
	context['reviews'] = reviews
	like_count = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['like_num'] = like_count
	dislike_count = Movie.objects.filter(imdb_id = movie_id, dislike_list__in = User.objects.all()).count()
	context['dislike_num'] = dislike_count
	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['m_also'] = get_people_also_liked_movies(movie_id, request.user)
	context['u_like'] = get_people_who_liked_this(movie_id, request.user)
	return render(request, 'movie.html', context)

def cast_list(request):
	context = {}
	return render(request, 'cast_list.html', context)

def review_list(request):
	context = {}
	return render(request, 'review_list.html', context)

def people_also_liked_list(request):
	context = {}
	return render(request, 'people_also_liked_list.html', context)

def people_who_liked_list(request):
	context = {}
	return render(request, 'people_who_liked_list.html', context)

def get_people_also_liked_movies(movie_id, current_user):

	m = Movie.objects.get(imdb_id = movie_id)
	u_list = m.like_list.exclude(username = current_user.username)

	m_list = []
	for u in u_list:
		m_list.extend(u.m_like.exclude(imdb_id = movie_id))

	counter=collections.Counter(m_list)
	print counter
	sorted_m_list = sorted(counter.items(), key=itemgetter(1))[::-1]
	print sorted_m_list

	movie_combos = []
	for m_tuple in sorted_m_list:
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
						'certificate' : m.certificate}
		movie_combos.append(movie_combo)

	return movie_combos

def get_people_who_liked_this(movie_id, current_user):

	m = Movie.objects.get(imdb_id = movie_id)
	users = m.like_list.exclude(username = current_user.username)

	return users


def person(request, person_id):
	context = {}
	context['search_form'] = SearchForm() 
	p = get_object_or_404(Person, person_id = person_id)
	context['p'] = p
	return render(request, 'person.html', context)

@login_required
def write_review(request,movie_id):
	context = {}
	context['search_form'] = SearchForm() 
	review_form = ReviewForm()
	context['review_form'] = review_form
	m = get_object_or_404(Movie, imdb_id = movie_id)
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
	context['m'] = movie_combo
	movie_be_reviewed = Movie.objects.get(imdb_id = movie_id)
	review_new = Review(movie = movie_be_reviewed, publisher = request.user)

	if request.method == 'GET':
		return redirect('/movie/' + movie_id);
		
	review_form = ReviewForm(request.POST, instance = review_new)

	if not review_form.is_valid():
		return redirect('/movie/' + movie_id);

	review_form.save()
	reviews = Review.objects.filter(movie = movie_be_reviewed).order_by('id').reverse()
	context['reviews'] = reviews

	like_count = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['like_num'] = like_count
	dislike_count = Movie.objects.filter(imdb_id = movie_id, dislike_list__in = User.objects.all()).count()
	context['dislike_num'] = dislike_count
	return render(request, 'movie.html', context)

@login_required
def new_review(request,movie_id):
	context = {}
	review_form = ReviewForm()
	context['review_form'] = review_form
	m = get_object_or_404(Movie, imdb_id = movie_id)
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
	context['m'] = movie_combo
	like_count = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()
	context['like_num'] = like_count
	dislike_count = Movie.objects.filter(imdb_id = movie_id, dislike_list__in = User.objects.all()).count()
	context['dislike_num'] = dislike_count
	return render(request, 'write_review.html', context)

@login_required
def like(request, movie_id):
	context = {}
	context['search_form'] = SearchForm()
	m = get_object_or_404(Movie, imdb_id = movie_id)
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
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['review_form'] = review_form
	movie_be_reviewed = Movie.objects.get(imdb_id = movie_id)
	reviews = Review.objects.filter(movie = movie_be_reviewed).order_by('id').reverse()
	context['reviews'] = reviews 

	current_user = request.user
	movie_be_like = Movie.objects.get(imdb_id = movie_id)
	if current_user in movie_be_like.like_list.all():
		movie_be_like.like_list.remove(request.user)
	else:
		movie_be_like.like_list.add(request.user)
	
	like_count = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()

	context['like_num'] = like_count
	dislike_count = Movie.objects.filter(imdb_id = movie_id, dislike_list__in = User.objects.all()).count()
	context['dislike_num'] = dislike_count

	return redirect('/movie/' + movie_id)


@login_required
def dislike(request, movie_id):
	context = {}
	context['search_form'] = SearchForm()
	m = get_object_or_404(Movie, imdb_id = movie_id)
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
	review_form = ReviewForm()
	context['m'] = movie_combo
	context['review_form'] = review_form
	movie_be_reviewed = Movie.objects.get(imdb_id = movie_id)
	reviews = Review.objects.filter(movie = movie_be_reviewed).order_by('id').reverse()
	context['reviews'] = reviews 

	current_user = request.user
	movie_be_dislike = Movie.objects.get(imdb_id = movie_id)
	if current_user in movie_be_dislike.dislike_list.all():
		movie_be_dislike.dislike_list.remove(request.user)
	else:
		movie_be_dislike.dislike_list.add(request.user)
	like_count = Movie.objects.filter(imdb_id = movie_id, like_list__in = User.objects.all()).count()

	context['like_num'] = like_count
	dislike_count = Movie.objects.filter(imdb_id = movie_id, dislike_list__in = User.objects.all()).count()
	context['dislike_num'] = dislike_count
	return render(request, 'movie.html', context)

def review(request,review_id):
	context = {}
	comment_form = CommentForm()
	context['comment_form'] = comment_form 
	context['search_form'] = SearchForm()
	review_be_checked = Review.objects.get(id = review_id)
	context['review'] = review_be_checked
	comments = Comment.objects.filter(review = review_be_checked).order_by('id').reverse()
	context['comments'] = comments
	m = get_object_or_404(Movie, reviews_included  = review_be_checked)
	print m.title
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
	context['m'] = movie_combo
	return render(request, 'review.html', context)

@login_required
def write_comment(request,review_id):
	context = {}
	review_be_comment = Review.objects.get(id = review_id)
	print review_be_comment.id
	comment_new = Comment(review = review_be_comment, publisher = request.user)

	if request.method == 'GET':
		return redirect('/review/' + review_id);
		
	comment_form = CommentForm(request.POST, instance = comment_new)

	if not comment_form.is_valid():
		return redirect('/review/' + review_id);

	comment_form.save()
	comments = Comment.objects.filter(review = review_be_comment).order_by('id').reverse()
	comments_num = Comment.objects.filter(review = review_be_comment)
	context['comments'] = comments
	context['review'] = review_be_comment
	context['comments_num'] = comments_num
	# m = Movie.objects.get(reviews_included  = review_be_comment)
	m = get_object_or_404(Movie, reviews_included  = review_be_comment)
	print m.title
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
	context['m'] = movie_combo
	return render(request, 'review.html', context)

def profile(request):
	context = {}
	context['search_form'] = SearchForm() 
	return render(request, 'profile.html', context)


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

	# 
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

	# loginform = LoginForm(request.POST)
	# if not loginform.is_valid():
	# 	print 334
	# 	return redirect('/')

	return login(request,redirect_field_name='/',
							template_name='home.html',
							authentication_form=LoginForm,
							extra_context={'login_form':LoginForm,'regis_form':RegistrationForm})


@login_required
def log_out(request):
	# next = next_page
	return logout(request,next_page='/')