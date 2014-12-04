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
from views import get_form_context

max_id = 9223372036854775807
# Create your views here.
def profile(request, user_id):
	if int(user_id) > max_id:
		raise Http404
	
	context = {}
	context.update(get_form_context())
	context['request'] = request
	context['user'] = request.user
	user_be_view = get_object_or_404(User,id = user_id)

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

@transaction.atomic
@login_required
def intro(request, user_id):
	if int(user_id) > max_id:
		raise Http404
	if request.method == 'GET':
		return redirect('/profile/' + user_id)

	profile_new = Profile.objects.filter(user = request.user)
	if profile_new.count() == 0:
		profile_new = Profile(user = request.user)
	else:
		profile_new = get_object_or_404(Profile, user = request.user)

	intro_form = IntroForm(request.POST, instance = profile_new)

	if not intro_form.is_valid():
		return redirect('/profile/' + user_id)

	intro_form.save()
	return redirect('/profile/' + user_id)

@transaction.atomic
@login_required
def profile_photo(request, user_id):
	if int(user_id) > max_id:
		raise Http404
	if request.method == 'GET':
		return redirect('/profile/' + user_id)

	profile_new = Profile.objects.filter(user = request.user)
	
	if profile_new.count() == 0:
		profile_new = Profile(user = request.user)
	else:
		profile_new = get_object_or_404(Profile, user = request.user)

	photo_form = PhotoForm(request.POST, request.FILES, instance = profile_new)

	if not photo_form.is_valid():
		return redirect('/profile/' + user_id)

	photo_form.save()
	return redirect('/profile/' + user_id)

@transaction.atomic
@login_required
def follow(request, user_id):
	if int(user_id) > max_id:
		raise Http404
	user_be_followed = get_object_or_404(User, id = user_id)

	profile_of_login_user = get_object_or_404(Profile, user = request.user)
	if user_be_followed in profile_of_login_user.users_followed.all():
		profile_of_login_user.users_followed.remove(user_be_followed)
		response_text = 'follow'
	else:
		profile_of_login_user.users_followed.add(user_be_followed)
		response_text = 'unfollow'

	return HttpResponse(response_text)


def get_photo(request, user_id):
	if int(user_id) > max_id:
		raise Http404
	profile = get_object_or_404(Profile, user__id = user_id)
	if not profile.photo:
		raise Http404
	
	content_type = guess_type(profile.photo.name)
	return HttpResponse(profile.photo, content_type = content_type)
