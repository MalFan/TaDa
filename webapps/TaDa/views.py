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
from django.utils.encoding import smart_bytes
from django.db import transaction

import imdb
import collections
from operator import itemgetter
import re

from models import *
from forms import *

max_id = 9223372036854775807
# Create your views here.
def get_form_context():
	context = {}
	context['regis_form'] = RegistrationForm()
	context['login_form'] = LoginForm()
	context['search_form'] = SearchForm()	
	return context

# Improve search feature
# http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
	    and grouping quoted words together.
	    Example:
	    
	    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
	    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

# Used for searching action
def get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
	    aims to search keywords within a model by testing the given search fields.

	'''
	query = None # Query to search for every search term        
	terms = normalize_query(query_string)
	if terms == []:
		or_query = None
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: terms})
			if or_query is None:
			    or_query = q
			else:
			    or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	else:
		for term in terms:
			or_query = None # Query to search for a given term in each field
			for field_name in search_fields:
				q = Q(**{"%s__icontains" % field_name: term})
				if or_query is None:
				    or_query = q
				else:
				    or_query = or_query | q
			if query is None:
				query = or_query
			else:
				query = query & or_query
	return query

def search(request):
	context = {}
	context.update(get_form_context())
	search_form = SearchForm(request.GET) 
	
	if not search_form.is_valid():
		context.update(get_form_context())
		return  render(request, 'search.html', context)

	context['search_form'] = search_form
	keywords = search_form.cleaned_data['search_content']
	search_type = search_form.cleaned_data['search_type']

	if search_type == 'all':
		movie_query = get_query(keywords, ['title',])
		movies = Movie.objects.filter(movie_query)

		person_query = get_query(keywords, ['name',])
		persons = Person.objects.filter(person_query, has_full_info = True)

		user_query = get_query(keywords, ['username',])
		users = User.objects.filter(user_query)

		context['movie_combos'] = movies
		context['person_combos'] = persons
		context['user_combos'] = users

	elif search_type == 'movies':
		movie_query = get_query(keywords, ['title',])
		movies = Movie.objects.filter(movie_query)

		context['movie_combos'] = movies
	elif search_type == 'names':
		person_query = get_query(keywords, ['name',])
		persons = Person.objects.filter(person_query, has_full_info = True)

		context['person_combos'] = persons
	elif search_type == 'users':
		user_query = get_query(keywords, ['username',])
		users = User.objects.filter(user_query)
		
		context['user_combos'] = users

	return render(request, 'search.html', context)


def movie(request, movie_id):
	context = {}
	context.update(get_form_context())
	m = get_object_or_404(Movie, imdb_id = movie_id)

	if len(m.cast_list.all()) > 15:
		context['is_cast_full'] = 'true'

	review_form = ReviewForm()
	context['m'] = m
	context['m_cast_character_list'] = zip(m.cast_list.all()[:15], m.character_list.all()[:15])
	context['review_form'] = review_form
	movie_be_reviewed = get_object_or_404(Movie, imdb_id = movie_id)
	reviews = Review.objects.filter(movie = movie_be_reviewed).order_by('score').reverse()
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

	context['m_also'] = get_people_also_liked_movies(movie_id, request.user)
	if len(context['m_also']) > 5:
		context['m_also'] = context['m_also'][:5]
		context['is_m_also_full'] = 'true'
		
	context['u_like'] = get_people_who_liked_this(movie_id, request.user)
	if len(context['u_like']) > 5:
		context['u_like'] = context['m_also'][:5]
		context['is_u_like_full'] = 'true'

	return render(request, 'movie.html', context)

def get_people_also_liked_movies(movie_id, current_user):

	m = get_object_or_404(Movie, imdb_id = movie_id)
	u_list = m.like_list.exclude(username = current_user.username)

	m_list = []
	for u in u_list:
		m_list.extend(u.m_like.exclude(imdb_id = movie_id))

	counter=collections.Counter(m_list)
	sorted_m_list = sorted(counter.items(), key=itemgetter(1))[::-1]

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
						'certificate' : m.certificate,
						'ticket_url' : m.ticket_url}
		movie_combos.append(movie_combo)

	return movie_combos

def get_people_who_liked_this(movie_id, current_user):

	m = get_object_or_404(Movie, imdb_id = movie_id)
	users = m.like_list.exclude(username = current_user.username)

	return users


def person(request, person_id):
	context = {}
	context.update(get_form_context())
	p = get_object_or_404(Person, person_id = person_id)
	context['p'] = p
	context['recent_works'] = get_recent_works(person_id)
	return render(request, 'person.html', context)

def get_recent_works(person_id):
	
	p =  get_object_or_404(Person, person_id = person_id)
	movies = Movie.objects.filter(Q(cast_list__in=[p]) | \
			Q(producer_list__in=[p]) | \
			Q(writer_list__in=[p]) | \
			Q(director_list__in=[p])).distinct().order_by('-year')
	return movies


@transaction.atomic
@login_required
def like(request, movie_id):
	current_user = request.user
	movie_be_like = get_object_or_404(Movie, imdb_id = movie_id)
	# Update the vector
	vector_str = smart_bytes(movie_be_like.vector, encoding='utf-8', strings_only=False, errors='strict')
	vector = vector_str.split(',')
	# Update the user_vector
	user_vector_str = smart_bytes(current_user.profile.user_vector, encoding='utf-8', strings_only=False, errors='strict')
	user_vector = user_vector_str.split(',')

	if current_user in movie_be_like.like_list.all():
		movie_be_like.like_list.remove(request.user)
		response_text = -1
		# Update the vector
		vector[current_user.id - 1] = '0'
		user_vector[movie_be_like.id - 1] = '0'
	else:		
		movie_be_like.like_list.add(request.user)
		response_text = 1
		# Update the vector
		vector[current_user.id - 1] = '1'
		user_vector[movie_be_like.id - 1] = '1'

		if current_user in movie_be_like.dislike_list.all():
			movie_be_like.dislike_list.remove(request.user)

	# Update the vector
	vector_str = ','.join(vector)
	movie_be_like.vector = vector_str
	movie_be_like.save()
	# Update the user_vector
	user_vector_str = ','.join(user_vector)
	current_user.profile.user_vector = user_vector_str
	current_user.profile.save()

	return HttpResponse(response_text)

@transaction.atomic
@login_required
def dislike(request, movie_id):
	current_user = request.user
	movie_be_dislike = get_object_or_404(Movie, imdb_id = movie_id)
	# Update the vector
	vector_str = smart_bytes(movie_be_dislike.vector, encoding='utf-8', strings_only=False, errors='strict')
	vector = vector_str.split(',')
	# Update the user_vector
	user_vector_str = smart_bytes(current_user.profile.user_vector, encoding='utf-8', strings_only=False, errors='strict')
	user_vector = user_vector_str.split(',')

	if current_user in movie_be_dislike.dislike_list.all():
		movie_be_dislike.dislike_list.remove(request.user)
		response_text = -1
		# Update the vector
		vector[current_user.id - 1] = '0'
		user_vector[movie_be_dislike.id - 1] = '0'
	else:
		movie_be_dislike.dislike_list.add(request.user)
		response_text = 1
		# Update the vector
		vector[current_user.id - 1] = '-1'
		user_vector[movie_be_dislike.id - 1] = '-1'

		if current_user in movie_be_dislike.like_list.all():
			movie_be_dislike.like_list.remove(request.user)

	# Update the vector
	vector_str = ','.join(vector)
	movie_be_dislike.vector = vector_str
	movie_be_dislike.save()
	# Update the user_vector
	user_vector_str = ','.join(user_vector)
	current_user.profile.user_vector = user_vector_str
	current_user.profile.save()

	return HttpResponse(response_text)

@transaction.atomic
@login_required
def write_review(request,movie_id):
	if request.method == 'GET':
		return redirect('/movie/' + movie_id)

	context = {}
	review_form = ReviewForm()
	movie_be_reviewed = get_object_or_404(Movie, imdb_id = movie_id)
	review_new = Review(movie = movie_be_reviewed, publisher = request.user)
	
	review_form = ReviewForm(request.POST, instance = review_new)

	if not review_form.is_valid():
		return redirect('/movie/' + movie_id)

	review_form.save()

	return redirect('/movie/'+movie_id)

@transaction.atomic
@login_required
def new_review(request,movie_id):
	context = {}
	context.update(get_form_context())
	review_form = ReviewForm()
	context['review_form'] = review_form
	m = get_object_or_404(Movie, imdb_id = movie_id)
	
	context['m'] = m
	like_count = m.like_list.all().count()
	context['like_num'] = like_count
	dislike_count = m.dislike_list.all().count()
	context['dislike_num'] = dislike_count
	return render(request, 'write_review.html', context)

@transaction.atomic
@login_required
def delete_review(request,review_id):

	if int(review_id) >= max_id:
		raise Http404
	review_be_delete = get_object_or_404(Review, id = review_id)
	movie_be_reviewed = get_object_or_404(Movie, reviews_included = review_be_delete)
	
	review_be_delete.delete()
	return redirect('/movie/'+movie_be_reviewed.imdb_id)

@transaction.atomic
@login_required
def delete_review_page(request,review_id):
	if int(review_id) >= max_id:
		raise Http404
	review_be_delete = get_object_or_404(Review, id = review_id)
	movie_be_reviewed = get_object_or_404(Movie, reviews_included = review_be_delete)
	movie_id = movie_be_reviewed.imdb_id
	review_be_delete.delete()
	return redirect('/movie/' + movie_id)

def review(request,review_id):
	if int(review_id) >= max_id:
		raise Http404
	context = {}
	context.update(get_form_context())
	comment_form = CommentForm()
	context['comment_form'] = comment_form 
	review_be_checked = get_object_or_404(Review, id = review_id)
	context['review'] = review_be_checked
	comments = Comment.objects.filter(review = review_be_checked).order_by('id').reverse()
	context['comments'] = comments
	m = get_object_or_404(Movie, reviews_included  = review_be_checked)

	context['m'] = m
	like_count = Movie.objects.filter(imdb_id = m.imdb_id, like_list__in = User.objects.all()).count()
	context['like_num'] = like_count

	review_like_list = get_object_or_404(Review, id = review_id).like_list.all()
	if request.user in review_like_list:
		context['review_like_status'] = 'liked'
	context['review_like_num'] = review_like_list.count()

	review_dislike_list = get_object_or_404(Review, id = review_id).dislike_list.all()
	if request.user in review_dislike_list:
		context['review_dislike_status'] = 'disliked'
	context['review_dislike_num'] = review_dislike_list.count()

	return render(request, 'review.html', context)

@transaction.atomic
def update_review_score(review_id):

	review_be_scored = get_object_or_404(Review, id = review_id)
	useful_num = float(get_object_or_404(Review, id = review_id).like_list.all().count())
	useless_num = float(get_object_or_404(Review, id = review_id).dislike_list.all().count())
	comment_num = float(review_be_scored.comments_included.all().count()) + 1
	score = (useful_num + 1) / (useful_num + useless_num + 1) * pow(comment_num, 0.1)

	review_be_scored.score = score

	review_be_scored.save()

@transaction.atomic
@login_required
def write_comment(request, review_id):
	if int(review_id) >= max_id:
		raise Http404
	
	if request.method == 'GET':
		return redirect('/review/' + review_id)
	
	context = {}
	context.update(get_form_context())
	review_be_comment = get_object_or_404(Review, id = review_id)
	comment_new = Comment(review = review_be_comment, publisher = request.user)
	comment_form = CommentForm(request.POST, instance = comment_new)

	if not comment_form.is_valid():
		return redirect('/review/' + review_id)

	comment_form.save()

	context['comment'] = comment_new
	update_review_score(review_id)

	notification = Notification(comment = comment_new, review = review_be_comment)
	notification.save()
	
	return render(request, 'write_comment.html', context)

@transaction.atomic
@login_required
def delete_comment(request,comment_id):
	if int(comment_id) >= max_id:
		raise Http404
	comment_be_delete = get_object_or_404(Comment, id = comment_id)
	review_be_commented = get_object_or_404(Review, comments_included = comment_be_delete)
	
	comment_be_delete.delete()
	return redirect('/review/' + str(review_be_commented.id))

@transaction.atomic
@login_required
def review_like(request,review_id):
	if int(review_id) >= max_id:
		raise Http404
	current_user = request.user
	review_be_like = get_object_or_404(Review, id = review_id)
	if current_user in review_be_like.like_list.all():
		review_be_like.like_list.remove(request.user)
		response_text = -1
	else:
		review_be_like.like_list.add(request.user)
		response_text = 1
		if current_user in review_be_like.dislike_list.all():
			review_be_like.dislike_list.remove(request.user)

	update_review_score(review_id)

	return HttpResponse(response_text)

@transaction.atomic
@login_required
def review_dislike(request,review_id):
	if int(review_id) >= max_id:
		raise Http404
	current_user = request.user
	review_be_dislike = get_object_or_404(Review, id = review_id)
	if current_user in review_be_dislike.dislike_list.all():
		review_be_dislike.dislike_list.remove(request.user)
		response_text = -1
	else:
		review_be_dislike.dislike_list.add(request.user)
		response_text = 1
		if current_user in review_be_dislike.like_list.all():
			review_be_dislike.like_list.remove(request.user)

	update_review_score(review_id)

	return HttpResponse(response_text)

@transaction.atomic
@login_required
def check_comments(request):
	context = {}
	current_user = request.user

	notifications = Notification.objects.filter(review__publisher=current_user)

	reviews = Review.objects.filter(notifications_included__in=notifications).distinct()
	current_user.profile.last_check_time = timezone.now()

	current_user.profile.save()

	context['reviews'] = reviews

	return render(request, 'append_notification_list.html', context)

@transaction.atomic
@login_required
def delete_notification(request, review_id):
	if int(review_id) >= max_id:
		raise Http404
	current_user = request.user
	notifications = Notification.objects.filter(review__publisher=current_user, review__id=review_id)
	notifications.delete()

	return redirect('/review/' + review_id + '#comment-list')