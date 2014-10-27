from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User)
	intro = models.CharField(max_length=255, blank=True)
	photo = models.ImageField(
			upload_to='profile-photos', 
			default='profile-photos/user_default.png') # attrs to be modified
	movies_liked = models.ManyToManyField(Movie, related_name='', blank=True) # attrs to be modified
	users_followed = models.ManyToManyField(User, related_name='', blank=True) # attrs to be modified

	def __unicode__(self):
		return self.user.username


class Movie(models.Model):
	name = models.CharField(max_length=255)
	year = models.CharField(max_length=4)
	cover = models.ImageField(upload_to='movie-cover', blank=True) # attrs to be modified
	# director = models.CharField(max_length=255)
	# cast = models.ManyToManyField(Star, related_name='', blank=True) # attrs to be modified
	storyline = models.CharField(max_length=1024)
	category = models.ManyToManyField(Category, related_name='', blank=True) # attrs to be modified
	tag = models.ManyToManyField(Tag, related_name='', blank=True) # attrs to be modified

	def __unicode__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name


class Review(models.Model):
	pub_time = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	text = models.CharField(max_length=8192)
	publisher = models.ForeignKey(User)

	def __unicode__(self):
		return self.title


class Comment(models.Model):
	pub_time = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=4096)
	publisher = models.ForeignKey(User)
	review = models.ForeignKey(Review)

	def __unicode__(self):
		return self.text

