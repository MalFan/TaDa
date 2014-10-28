from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, primary_key = True)
	intro = models.CharField(max_length=255, blank=True)
	photo = models.ImageField(
			upload_to='profile-photos', 
			default='profile-photos/user_default.png') # attrs to be modified
	movies_liked = models.ManyToManyField(Movie, related_name='', blank=True) # attrs to be modified
	movies_disliked = models.ManyToManyField(Movie, related_name='', blank=True) # attrs to be modified
	users_followed = models.ManyToManyField(User, related_name='', blank=True) # attrs to be modified

	def __unicode__(self):
		return self.user.username


class Movie(models.Model):
	name = models.CharField(max_length=255)
	year = models.CharField(max_length=4)
	date = models.DateField()
	isInTheater = models.NullBooleanField()
	cover = models.ImageField(upload_to='movie-cover', blank=True) # attrs to be modified
	director = models.ManyToManyField(Person, related_name = 'directing', blank=True)	
	writer = models.ManyToManyField(Person, related_name = 'writing', blank=True)
	cast = models.ManyToManyField(Person, related_name='acting', blank=True) # attrs to be modified
	storyline = models.CharField(max_length=1024)
	genres = models.ManyToManyField(Genre, related_name='including_movies', blank=True) # attrs to be modified
	certificate = models.CharField(max_length=10, blank=True)
	# tag = models.ManyToManyField(Tag, related_name='', blank=True) # attrs to be modified

	def __unicode__(self):
		return self.name


class Genre(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class People(models.Model):
	name = models.CharField(max_length=255)
	dob = models.DateField()
	bio = models.CharField(max_length=1024)	
	photo = models.ImageField(upload_to='people', blank=True)

	def __unicode__(self):
		return self.name

class Review(models.Model):
	pub_time = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	text = models.CharField(max_length=8192)
	movie = models.ForeignKey(Movie, related_name = 'including_reviews')
	publisher = models.ForeignKey(User, related_name = 'publishing')

	def __unicode__(self):
		return self.title


class Comment(models.Model):
	pub_time = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=4096)
	publisher = models.ForeignKey(User, related_name='publishing')
	review = models.ForeignKey(Review, related_name = 'including_comments')

	def __unicode__(self):
		return self.text

