from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth.views import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse, Http404
from mimetypes import guess_type

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
	context['movie_combos'] = get_recommend_movies()
	context['next_page'] = '/recommend-movie'
	return render(request, 'recommend_movie.html', context)
	
def get_recommend_movies():
	movies = []
	movies = Movie.objects.all().annotate(num_likes=Count('like_list')).order_by('num_likes').reverse()[:15]
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
			'cast_character_list' : zip(m.cast_list.all()[:15], m.character_list.all()[:15]),
			'storyline' : m.short_storyline,
			'genre_list' : m.genre_list.all(),
			'certificate' : m.certificate}

	if len(m.cast_list.all()) > 15:
		context['is_cast_full'] = 'true'

	review_form = ReviewForm()
	context['m'] = movie_combo
	context['review_form'] = review_form
	movie_be_reviewed = Movie.objects.get(imdb_id = movie_id)
	reviews = Review.objects.filter(movie = movie_be_reviewed).order_by('id').reverse()
	if len(reviews) > 5:
		reviews = reviews[:5]
		context['is_review_full'] = 'true'
	context['reviews'] = reviews

	like_list = get_object_or_404(Movie, imdb_id = movie_id).like_list.all()
	if request.user in like_list:
		context['like_status'] = 'liked'
	context['like_num'] = like_list.count()


	dislike_list = get_object_or_404(Movie, imdb_id = movie_id).dislike_list.all()
	if request.user in dislike_list:
		context['dislike_status'] = 'disliked'
	context['dislike_num'] = dislike_list.count()

	regis_form = RegistrationForm()
	login_form = LoginForm()
	context['regis_form'] = regis_form
	context['login_form'] = login_form
	context['m_also'] = get_people_also_liked_movies(movie_id, request.user)
	if len(context['m_also']) > 5:
		context['m_also'] = context['m_also'][:5]
		context['is_m_also_full'] = 'true'
		
	context['u_like'] = get_people_who_liked_this(movie_id, request.user)
	if len(context['u_like']) > 5:
		context['u_like'] = context['m_also'][:5]
		context['is_u_like_full'] = 'true'

	return render(request, 'movie.html', context)

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

def people_also_liked_list(request,movie_id):
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
	context['recent_works'] = get_recent_works(person_id)
	return render(request, 'person.html', context)

def get_recent_works(person_id):
	
	p =  Person.objects.get(person_id = person_id)
	movies = Movie.objects.filter(Q(cast_list__in=[p]) | \
			Q(producer_list__in=[p]) | \
			Q(writer_list__in=[p]) | \
			Q(director_list__in=[p])).distinct().order_by('-year')
	return movies


@login_required
def write_review(request,movie_id):
	if request.method == 'GET':
		return redirect('/movie/' + movie_id);

	context = {}
	review_form = ReviewForm()
	movie_be_reviewed = get_object_or_404(Movie, imdb_id = movie_id)
	review_new = Review(movie = movie_be_reviewed, publisher = request.user)
	
	review_form = ReviewForm(request.POST, instance = review_new)

	if not review_form.is_valid():
		return redirect('/movie/' + movie_id);

	review_form.save()

	return redirect('/movie/'+movie_id)

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
	current_user = request.user
	movie_be_like = Movie.objects.get(imdb_id = movie_id)
	if current_user in movie_be_like.like_list.all():
		movie_be_like.like_list.remove(request.user)
		response_text = -1
	else:
		movie_be_like.like_list.add(request.user)
		response_text = 1

	# return redirect('/movie/' + movie_id)

	return HttpResponse(response_text)

@login_required
def dislike(request, movie_id):
	current_user = request.user
	movie_be_dislike = Movie.objects.get(imdb_id = movie_id)
	if current_user in movie_be_dislike.dislike_list.all():
		movie_be_dislike.dislike_list.remove(request.user)
		response_text = -1
	else:
		movie_be_dislike.dislike_list.add(request.user)
		response_text = 1
	
	# return redirect('/movie/' + movie_id)
	return HttpResponse(response_text)


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
	like_count = Movie.objects.filter(imdb_id = m.imdb_id, like_list__in = User.objects.all()).count()
	context['like_num'] = like_count

	review_like_list = get_object_or_404(Review, id = review_id).like_list.all()
	if request.user in review_like_list:
		context['review_like_status'] = 'liked'
	context['review_like_num'] = review_like_list.count

	review_dislike_list = get_object_or_404(Review, id = review_id).dislike_list.all()
	if request.user in review_dislike_list:
		context['review_dislike_status'] = 'disliked'
	context['review_dislike_num'] = review_dislike_list.count

	return render(request, 'review.html', context)

@login_required
def write_comment(request, review_id):	
	context = {}
	review_be_comment = Review.objects.get(id = review_id)
	comment_new = Comment(review = review_be_comment, publisher = request.user)
	comment_form = CommentForm(request.POST, instance = comment_new)

	if not comment_form.is_valid():
		return redirect('/review/' + review_id)

	comment_form.save()

	context['comment'] = comment_new
	
	return render(request, 'write_comment.html', context)

@login_required
def review_like(request,review_id):
	current_user = request.user
	review_be_like = get_object_or_404(Review, id = review_id)
	if current_user in review_be_like.like_list.all():
		review_be_like.like_list.remove(request.user)
	else:
		review_be_like.like_list.add(request.user)

	return redirect('/review/' + review_id)

@login_required
def review_dislike(request,review_id):
	current_user = request.user
	review_be_dislike = get_object_or_404(Review, id = review_id)
	if current_user in review_be_dislike.dislike_list.all():
		review_be_dislike.dislike_list.remove(request.user)
	else:
		review_be_dislike.dislike_list.add(request.user)

	return redirect('/review/' + review_id)

def profile(request, user_id):
	context = {}

	context['user'] = request.user
	user_be_view = get_object_or_404(User,id = user_id)
	print user_be_view.username

	if Profile.objects.filter(user = user_be_view).count() == 0:
		profile = Profile(user = user_be_view)
		profile.save()

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
		profile = Profile.objects.get(user = user_be_view)
		context['profile'] = profile
		# print profile.photo
	# context['photo_form'] = PhotoForm()
	context['search_form'] = SearchForm()
	user_be_followed = get_object_or_404(User, id = user_id)
	if request.user.username:
		profile_of_login_user = get_object_or_404(Profile, user = request.user)
		if user_be_followed in profile_of_login_user.users_followed.all():
			context['follow_text'] = 'unfollow'
		else:
			context['follow_text'] = 'follow'
	else:
		context['follow_text'] = 'follow'
	return render(request, 'profile.html', context)

@login_required
def intro(request, user_id):

	if request.method == 'GET':
		return redirect('/profile/' + user_id)

	profile_new = Profile.objects.filter(user = request.user)
	if profile_new.count() == 0:
		profile_new = Profile(user = request.user)
	else:
		profile_new = Profile.objects.get(user = request.user)

	intro_form = IntroForm(request.POST, instance = profile_new)

	if not intro_form.is_valid():
		return redirect('/profile/' + user_id)

	intro_form.save()
	return redirect('/profile/' + user_id)

@login_required
def profile_photo(request, user_id):

	if request.method == 'GET':
		return redirect('/profile/' + user_id)

	profile_new = Profile.objects.filter(user = request.user)
	
	if profile_new.count() == 0:
		profile_new = Profile(user = request.user)
	else:
		profile_new = Profile.objects.get(user = request.user)

	print profile_new.user.username

	photo_form = PhotoForm(request.POST, request.FILES, instance = profile_new)

	if not photo_form.is_valid():
		return redirect('/profile/' + user_id)

	photo_form.save()
	return redirect('/profile/' + user_id)

@login_required
def follow(request, user_id):
	user_be_followed = get_object_or_404(User, id = user_id)
	# print user_be_followed.username
	profile_of_login_user = get_object_or_404(Profile, user = request.user)
	if user_be_followed in profile_of_login_user.users_followed.all():
		profile_of_login_user.users_followed.remove(user_be_followed)
	else:
		profile_of_login_user.users_followed.add(user_be_followed)

	return redirect('/profile/' + user_id)

def get_photo(request, user_id):

	profile = get_object_or_404(Profile, user__id = user_id)
	if not profile.photo:
		raise Http404
	
	print profile.photo.name
	content_type = guess_type(profile.photo.name)
	print content_type
	return HttpResponse(profile.photo, content_type = content_type)

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
	
	profile = Profile(user = new_user)
	profile.save()
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