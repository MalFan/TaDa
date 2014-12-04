from django.conf.urls import patterns, include, url
from django.contrib import admin
from forms import *
from django.conf import settings

urlpatterns = patterns('',
	url(r'^admin$', 'TaDa.views_admin.admin_homepage', name='admin_homepage'),
	url(r'^admin-search$', 'TaDa.views_admin.admin_search', name='admin_search'),
	url(r'^admin-add-movie/(?P<movie_id>\d+)$', 'TaDa.views_admin.admin_add_movie', name='admin_add_movie'),
	url(r'^admin-add-person/(?P<person_id>\d+)$', 'TaDa.views_admin.admin_add_person', name='admin_add_person'),
	url(r'^admin-one-touch$', 'TaDa.views_admin.admin_one_touch', name='admin_one_touch'),
	
	url(r'^$','TaDa.views_home.home'),
	url(r'^recommend-movie$','TaDa.views_home.recommend_movie'),
	url(r'^recommend-user$','TaDa.views_home.recommend_user'),
	
	url(r'^search$','TaDa.views.search'),
	url(r'^check-comments$', 'TaDa.views.check_comments', name='check_comments'),
	url(r'^delete-notification/(?P<review_id>\d+)$','TaDa.views.delete_notification', name='delete_notification'),

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
	url(r'^delete_review/(?P<review_id>\d+)$','TaDa.views.delete_review',name='delete_review'),
	url(r'^delete_comment/(?P<comment_id>\d+)$','TaDa.views.delete_comment',name='delete_comment'),
	url(r'^delete_review_page/(?P<review_id>\d+)$','TaDa.views.delete_review_page',name='delete_review_page'),

	url(r'^movie-cast-list/(?P<movie_id>\d+)$','TaDa.views_more.movie_cast_list'),
	url(r'^movie-review-list/(?P<movie_id>\d+)$','TaDa.views_more.movie_review_list'),
	url(r'^movie-people-also-liked-list/(?P<movie_id>\d+)$','TaDa.views_more.movie_people_also_liked_list'),
	url(r'^movie-people-who-liked-list/(?P<movie_id>\d+)$','TaDa.views_more.movie_people_who_liked_list'),

	url(r'^profile-movie-list/(?P<view_user_id>\d+)$','TaDa.views_more.profile_movie_list'),
	url(r'^profile-review-list/(?P<view_user_id>\d+)$','TaDa.views_more.profile_review_list'),
	url(r'^profile-following-list/(?P<view_user_id>\d+)$','TaDa.views_more.profile_following_list'),
	
	url(r'^profile/(?P<user_id>\d+)$','TaDa.views_profile.profile', name='profile'),
	url(r'^intro/(?P<user_id>\d+)$','TaDa.views_profile.intro', name='intro'),
	url(r'^profile_photo/(?P<user_id>\d+)$','TaDa.views_profile.profile_photo', name='profile_photo'),
	url(r'^get-photo/(?P<user_id>\d+)$','TaDa.views_profile.get_photo', name='get-photo'),
	url(r'^follow/(?P<user_id>\d+)$','TaDa.views_profile.follow', name='follow'),

	url(r'^register$','TaDa.views_account.register'),
	url(r'^login$', 'TaDa.views_account.log_in',name='login'),
	url(r'^logout$', 'TaDa.views_account.log_out', name='logout'),
	url(r'^send-reset-email$', 'TaDa.views_account.send_reset_email'),
	url(r'^password-reset$', 'TaDa.views_account.password_reset'),
	url(r'^email-password-send$', 'TaDa.views_account.email_receive_confirm',name='email-password-send'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$','TaDa.views_account.email_password_reset_confirm',
        name='password_reset_confirm'),
	url(r'^email-password-reset-complete$', 'django.contrib.auth.views.password_reset_complete',{'template_name':'password_reset_complete.html','extra_context':{'regis_form':RegistrationForm,'search_form':SearchForm,'login_form':LoginForm}}, name='email-password-reset-complete'),	
	url(r'^password-change$', 'TaDa.views_account.my_password_change'),
	url(r'^password-change-complete$', 'TaDa.views_account.password_change_complete',name="login-save-password-done"),
	

	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

)
