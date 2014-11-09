from django.conf.urls import patterns, include, url
from django.contrib import admin
from forms import *

urlpatterns = patterns('',
	url(r'^admin$', 'TaDa.views_admin.admin_homepage', name='admin_homepage'),
	url(r'^admin-search$', 'TaDa.views_admin.admin_search', name='admin_search'),
	url(r'^admin-add-movie/(?P<movie_id>\d+)$', 'TaDa.views_admin.admin_add_movie', name='admin_add_movie'),
	url(r'^admin-add-person/(?P<person_id>\d+)$', 'TaDa.views_admin.admin_add_person', name='admin_add_person'),
	
	url(r'^$','TaDa.views.home'),
	url(r'^recommend-movie$','TaDa.views.recommend_movie'),
	url(r'^search$','TaDa.views.search'),
	url(r'^movie$','TaDa.views.movie'),
	url(r'^person$','TaDa.views.person'),
	url(r'^review$','TaDa.views.review'),
	url(r'^write-review$','TaDa.views.write_review'),

	url(r'^profile$','TaDa.views.profile'),

	url(r'^register$','TaDa.views.register'),
	url(r'^login$', 'TaDa.views.log_in'),
	# url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'generic.html',
	# 	'redirect_field_name':'/',
 #        'authentication_form':LoginForm,'extra_context':{'regis_form':RegistrationForm}}),
	url(r'^logout$', 'TaDa.views.log_out', name='logout'),


)
