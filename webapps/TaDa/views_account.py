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
from django.contrib.auth.views import password_change, password_change_done
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
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
	print 111
	email_form = EmailEnterForm(request.POST)
	if not email_form.is_valid():
		return HttpResponse("failed")	
		# print 234
		# return password_reset(request,
		# 	post_reset_redirect=request.POST['next'],
		# 	password_reset_form=EmailEnterForm)

		# return HttpResponse("successful")

	print 222
	return password_reset(request,
							post_reset_redirect='email-password-send',
							password_reset_form=EmailEnterForm)
			
	#if email not exist
		#reutrn HttpResponse("failed")
	# if(True):
		
def email_receive_confirm(request):
	print 666
	return password_reset_done(request,
								template_name='home.html',
								extra_context={'regis_form':RegistrationForm,'search_form':SearchForm,'login_in':LoginForm,
								'request':request,'email_from':EmailEnterForm,'movie_combos':get_in_theater_movies()})

def email_password_reset_confirm(request,uidb64=None, token=None):
	context = {}
	# email_reset_confirm_form = EmailResetPasswordConfirmForm()
	# context['email_reset_confirm_form'] =  EmailResetPasswordConfirmForm()
	print 2333

	# return render(request, 'email_resetpass_confirm.html', context)
	return password_reset_confirm(request,uidb64=uidb64, token = token,
									template_name='password_reset.html',
									set_password_form= EmailResetPasswordForm,
									post_reset_redirect= 'email-password-reset-complete')


@login_required
def password_change(request,user_id):
	context = {}
	if(int(user_id) != request.user.id):
		return redirect("/")

	context = {}
	context['user'] = request.user
	context['pass_form'] = LoginChangePasswordForm(request.user)
	return render(request, "password_change.html", context);

@login_required
def password_change_complete(request,user_id):
	# context = {}
	context = {}
	pass_form = LoginChangePasswordForm(request.user,request.POST)
	context['pass_form'] = pass_form
	print pass_form

	if not pass_form.is_valid():
		return render(request, 'password_change.html', context)

	return password_change(request,
							template_name='password_change_complete.html',
							post_change_redirect='login-save-password-done',
							password_change_form=LoginChangePasswordForm)

	# return render(request, "password_change_complete.html", context);

@login_required
def login_password_change_done(request):
	return password_change_done(request,
								template_name='password_change_complete.html')
