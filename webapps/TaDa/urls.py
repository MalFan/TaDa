from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^admin$', 'TaDa.views.admin_homepage', name='admin_homepage'),
	url(r'^admin-search$', 'TaDa.views.admin_search', name='admin_search'),
	url(r'^admin-add-movie/(?P<movie_id>\d+)$', 'TaDa.views.admin_add_movie', name='admin_add_movie'),
	url(r'^admin-add-person/(?P<person_id>\d+)$', 'TaDa.views.admin_add_person', name='admin_add_person'),
	# url(r'^my-grumbls$', 'grumblr.views.my_grumbls', name='mygrumbls'),
	# url(r'^search$', 'grumblr.views.search', name='search'),
	# url(r'^add-grumbl/(?P<next>\w+)$', 'grumblr.views.add_grumbl', name='addgrumbl'),
	# url(r'^get-picture/(?P<grumbl_id>\d+)$', 'grumblr.views.get_picture', name='getpicture'),
	# url(r'^add-comment/(?P<grumbl_id>\d+)$', 'grumblr.views.add_comment', name='addcomment'),
	# url(r'^refresh$', 'grumblr.views.refresh', name='refresh'),

	# url(r'^dislike/(?P<grumbl_id>\d+)$', 'grumblr.views.dislike', name='dislike'),
	# url(r'^block/(?P<user_id>\d+)$', 'grumblr.views.block', name='block'),
	# url(r'^follow/(?P<user_id>\d+)$', 'grumblr.views.follow', name='follow'),

	# url(r'^my-following$', 'grumblr.views.my_following', name='myfollowing'),
	# url(r'^my-blocking$', 'grumblr.views.my_blocking', name='myblocking'),
	
	# url(r'^profile/(?P<user_id>\d+)$', 'grumblr.views.profile', name='profile'),
	# url(r'^edit-profile$', 'grumblr.views.edit_profile', name='editprofile'),
	# url(r'^get-photo/(?P<username>\w+)$', 'grumblr.views.get_photo', name='getphoto'),

	# url(r'^change-password$', 'grumblr.views.my_password_change', name='password_change'),
	# url(r'^password-changed$', 'grumblr.views.my_password_change_done', name='password_change_done'),


	# url(r'^forgot-password$', 'django.contrib.auth.views.password_reset', 
	# 	{'template_name':'password-reset-form.html', 'password_reset_form':MyPasswordResetForm}, name='password_reset'),
 #    	url(r'^password-reset-request$', 'django.contrib.auth.views.password_reset_done', 
 #    		{'template_name':'password-reset-done.html'}, name='password_reset_done'),
 #    	url(r'^password-reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
 #    		{'template_name':'password-reset-confirm.html', 'set_password_form':MySetPasswordForm}, name='password_reset_confirm'),
 #    	url(r'^password-reset-complete$', 'django.contrib.auth.views.password_reset_complete', 
 #    		{'template_name':'password-reset-complete.html'}, name='password_reset_complete'),
	



	# # Route for built-in authentication with our own custom login page
	# url(r'^login$', 'django.contrib.auth.views.login', 
	# 	{'template_name':'login.html', 
	# 	'authentication_form':LoginForm}, name='login'),
	# # Route to log out a user and send them back to the login page
	# url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	# url(r'^register$', 'grumblr.views.register', name='register'),
	# # The following URL should match any username valid in Django and
	# # any token produced by the default_token_generator
	# url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'grumblr.views.confirm_registration', name='confirm'),

)
