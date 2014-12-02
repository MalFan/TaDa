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

import imdb
import collections
from operator import itemgetter

from models import *
from forms import *
from views_home import *

# Create your views here.
def register(request):
	context = {}
	regis_form = RegistrationForm(request.POST)
	context['regis_form'] = regis_form
	context['search_form'] = SearchForm() 

	if request.method == 'GET':
		return redirect(request.POST['next'])

	if not regis_form.is_valid():
		return HttpResponse(regis_form.errors)

	new_user = User.objects.create_user(username=regis_form.cleaned_data['username'],
										email=regis_form.cleaned_data['email'],
										password=regis_form.cleaned_data['password1'])
	new_user.save()
	new_user = authenticate(username=regis_form.cleaned_data['username'],
										email=regis_form.cleaned_data['email'],
										password=regis_form.cleaned_data['password1'])
	
	profile = Profile(user = new_user)
	profile.save()

	movies_all = Movie.objects.all()
	for m in movies_all:
		s = smart_bytes(m.vector, encoding='utf-8', strings_only=False, errors='strict')
		s += ',0'
		m.vector = s
		m.save()

	auto_login(request, new_user)
	return eturn redirect(request.POST['next'])

def log_in(request):
	if request.method == 'GET':
		return redirect('/')

	login_form = LoginForm(request, data= request.POST)

	if login_form.is_valid():
		auto_login(request, login_form.get_user())
		return redirect(request.POST['next'])
	else:		
		return HttpResponse("error")
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

	# if request.method == 'GET':
	# 	return redirect('/')

	# # loginform = LoginForm(request.POST)
	# # if not loginform.is_valid():
	# # 	print 334
	# # 	return redirect('/')

	# return login(request,redirect_field_name='/',
	# 						template_name='home.html',
	# 						authentication_form=LoginForm,
	# 						extra_context={'login_form':LoginForm,'regis_form':RegistrationForm,'search_form':SearchForm,
	# 						'next':'/','movie_combos':get_in_theater_movies()})


@login_required
def log_out(request):
	# next = next_page
	return logout(request,next_page='/')