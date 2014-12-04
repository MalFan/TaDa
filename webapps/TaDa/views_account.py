from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auto_login
from django.contrib.auth.views import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import *
from django.db.models import Q, Count
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.utils import timezone 
from django.utils.encoding import smart_bytes
from django.contrib.auth.views import password_change, password_change_done
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
import imdb
import collections
from operator import itemgetter
from django.db import transaction

from models import *
from forms import *
from views_home import *
from views import 	get_form_context

# Create your views here.
@transaction.atomic
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
	return redirect(request.POST['next'])


def log_in(request):
	if request.method == 'GET':
		return redirect('/')

	login_form = LoginForm(request, data= request.POST)

	if login_form.is_valid():
		auto_login(request, login_form.get_user())
		return redirect(request.POST['next'])
	else:		
		return HttpResponse("error")

@login_required
def log_out(request):
	# next = next_page
	return logout(request,next_page='/')

def send_reset_email(request):
	email_form = EmailEnterForm(request.POST)
	if not email_form.is_valid():
		return HttpResponse("failed")	
		# print 234
		# return password_reset(request,
		# 	post_reset_redirect=request.POST['next'],
		# 	password_reset_form=EmailEnterForm)

		# return HttpResponse("successful")

	return password_reset(request,
							post_reset_redirect='email-password-send',
							password_reset_form=EmailEnterForm)
			
	#if email not exist
		#reutrn HttpResponse("failed")
	# if(True):

		
def email_receive_confirm(request):
	return password_reset_done(request,
								template_name='home.html',
								extra_context={'regis_form':RegistrationForm,'search_form':SearchForm,'login_form':LoginForm,
								'request':request,'email_from':EmailEnterForm,'movie_combos':get_in_theater_movies()})

@transaction.atomic
def email_password_reset_confirm(request,uidb64=None, token=None):
	context = {}
	return password_reset_confirm(request,uidb64=uidb64, token = token,
									template_name='password_reset.html',
									set_password_form= EmailResetPasswordForm,
									post_reset_redirect= 'email-password-reset-complete',
									extra_context = {'regis_form':RegistrationForm,'login_form':LoginForm})

@transaction.atomic
@login_required
def my_password_change(request):
	context = {}
	context['change_password_form'] = ChangePasswordForm()
	# if not change_password_form.is_valid():		
	# 	return HttpResponse("error")

	return render(request,'password_change.html',context);
	# return password_change(request,
	# 						template_name='password_change.html',
	# 						post_change_redirect='login-save-password-done',
	# 						password_change_form=LoginChangePasswordForm)

@transaction.atomic
@login_required
def password_change_complete(request):
	context = {}
	context.update(get_form_context())
	if request.method == 'GET':
		return redirect('/profile/'+str(request.user.id))

	change_password_form = ChangePasswordForm(request.POST)

	if not change_password_form.is_valid():
		return redirect('not valid')

	user_to_edit = authenticate(username= request.user.username, password=change_password_form.cleaned_data['old_password'])

	if user_to_edit is None:	
		return HttpResponse('error')

	user_to_edit.password = make_password(change_password_form.cleaned_data['new_password1'])		
	user_to_edit.save()
	
	user_editted = authenticate(username= user_to_edit.username, password=change_password_form.cleaned_data['new_password1'])
	auto_login(request, user_editted)
	return render(request, 'password_change_complete.html', context)