from django.shortcuts import render
import imdb

from models import *
# from forms import *

# Create your views here.
def home(request):
	context = {}
	return render(request, 'home.html', context)

def recommend_movie(request):
	context = {}
	return render(request, 'recommend_movie.html', context)

def search(request):
	context = {}
	return render(request, 'search.html', context)


