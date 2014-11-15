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
	url(r'^movie/(?P<movie_id>\d+)$','TaDa.views.movie'),
	url(r'^person/(?P<person_id>\d+)$','TaDa.views.person'),
	url(r'^review/(?P<review_id>\d+)$','TaDa.views.review',name='review'),
	url(r'^write-review/(?P<movie_id>\d+)$','TaDa.views.write_review',name='write_review'),
	url(r'^new_review/(?P<movie_id>\d+)$','TaDa.views.new_review',name='new_review'),
	url(r'^like/(?P<movie_id>\d+)$','TaDa.views.like',name='like'),
	url(r'^dislike/(?P<movie_id>\d+)$','TaDa.views.dislike',name='dislike'),
	url(r'^write-comment/(?P<review_id>\d+)$','TaDa.views.write_comment',name='write-comment'),
	url(r'^review-like/(?P<review_id>\d+)$','TaDa.views.review_like',name='review-like'),
	url(r'^review-dislike/(?P<review_id>\d+)$','TaDa.views.review_dislike',name='review-dislike'),

	url(r'^cast-list/(?P<movie_id>\d+)$','TaDa.views.cast_list'),
	url(r'^review-list/(?P<movie_id>\d+)$','TaDa.views.review_list'),
	url(r'^people-also-liked-list/(?P<movie_id>\d+)$','TaDa.views.people_also_liked_list'),
	url(r'^people-who-liked-list/(?P<movie_id>\d+)$','TaDa.views.people_who_liked_list'),

	url(r'^profile/(?P<user_id>\d+)$','TaDa.views.profile', name='profile'),
	url(r'^intro/(?P<user_id>\d+)$','TaDa.views.intro', name='intro'),
	url(r'^profile_photo/(?P<user_id>\d+)$','TaDa.views.profile_photo', name='profile_photo'),
	url(r'^get-photo/(?P<user_id>\d+)$','TaDa.views.get_photo', name='get-photo'),
	url(r'^follow/(?P<user_id>\d+)$','TaDa.views.follow', name='follow'),

	url(r'^register$','TaDa.views.register'),
	url(r'^login$', 'TaDa.views.log_in',name='login'),
	# url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'generic.html',
	# 	'redirect_field_name':'/',
 #        'authentication_form':LoginForm,'extra_context':{'regis_form':RegistrationForm}}),
	url(r'^logout$', 'TaDa.views.log_out', name='logout'),


)
