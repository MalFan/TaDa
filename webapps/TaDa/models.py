from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Genre(models.Model):
	name = models.CharField(max_length = 255)

	def __unicode__(self):
		return self.name


class Person(models.Model):
	person_id = models.CharField(max_length = 16)
	name = models.CharField(max_length = 255)
	birthyear = models.CharField(max_length = 8, blank = True)
	bio = models.CharField(max_length = 1024, blank = True)	
	# photo = models.ImageField(upload_to = 'person-photos', blank = True)
	photo = models.CharField(max_length = 255, blank = True)
	has_full_info = models.BooleanField(default = False)
	def __unicode__(self):
		return self.name


class Movie(models.Model):
	imdb_id = models.CharField(max_length = 8)
	title = models.CharField(max_length = 255)
	year = models.CharField(max_length = 4, blank = True)
	duration = models.CharField(max_length = 8, blank = True)
	# cover = models.ImageField(upload_to = 'movie-cover', blank = True)
	cover = models.CharField(max_length = 255, blank = True)
	director_list = models.ManyToManyField(Person, related_name = 'directing', blank = True)	
	writer_list = models.ManyToManyField(Person, related_name = 'writing', blank = True)
	cast_list = models.ManyToManyField(Person, related_name = 'acting', blank = True) # First 14 people
	storyline = models.CharField(max_length = 1024, blank = True)
	short_storyline = models.CharField(max_length = 255, blank = True)
	genre_list = models.ManyToManyField(Genre, related_name = 'movies_included', blank = True)
	certificate = models.CharField(max_length = 10, blank = True)

	def __unicode__(self):
		return self.title


class Profile(models.Model):
	user = models.OneToOneField(User, primary_key = True)
	intro = models.CharField(max_length = 255, blank = True)
	photo = models.ImageField(
			upload_to = 'profile-photos', 
			default = 'profile-photos/user_default.png')
	movies_liked = models.ManyToManyField(Movie, related_name = 'liked_by', blank = True)
	movies_disliked = models.ManyToManyField(Movie, related_name = 'disliked_by', blank = True)
	users_followed = models.ManyToManyField(User, related_name = 'followed_by', blank = True)

	def __unicode__(self):
		return self.user.username


class Review(models.Model):
	pub_time = models.DateTimeField(auto_now_add = True)
	title = models.CharField(max_length = 255)
	text = models.CharField(max_length = 8192)
	publisher = models.ForeignKey(User, related_name = 'reviews_published')
	movie = models.ForeignKey(Movie, related_name = 'reviews_included')

	def __unicode__(self):
		return self.title


class Comment(models.Model):
	pub_time = models.DateTimeField(auto_now_add = True)
	text = models.CharField(max_length = 4096)
	publisher = models.ForeignKey(User, related_name = 'comments_published')
	review = models.ForeignKey(Review, related_name = 'comments_included')

	def __unicode__(self):
		return self.text