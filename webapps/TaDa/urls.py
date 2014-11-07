from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^admin$', 'TaDa.views_admin.admin_homepage', name='admin_homepage'),
	url(r'^admin-search$', 'TaDa.views_admin.admin_search', name='admin_search'),
	url(r'^admin-add-movie/(?P<movie_id>\d+)$', 'TaDa.views_admin.admin_add_movie', name='admin_add_movie'),
	url(r'^admin-add-person/(?P<person_id>\d+)$', 'TaDa.views_admin.admin_add_person', name='admin_add_person'),
	
	url(r'^$','TaDa.views.home'),
	url(r'^recommend-movie$','TaDa.views.recommend_movie'),
	url(r'^search$','TaDa.views.search'),

)
