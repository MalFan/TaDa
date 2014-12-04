from django.shortcuts import render, redirect
from django.conf import settings
from django.db import transaction
from django.utils.encoding import *
import imdb
import numpy as np

from models import *
from views_tickets import *
import urllib
import os

# Create your views here.
def admin_homepage(request):
	context = {}
	return render(request, 'admin_homepage.html', context)


def admin_search(request):
	context = {}
	i = imdb.IMDb()
	movie_list = i.search_movie(request.GET['search'])

	context['movie_list'] = movie_list

	return render(request, 'admin_homepage.html', context)

@transaction.atomic
def update_vector_all(movie):
	user_num = User.objects.all().count()
	vector = np.asarray([0] * user_num)

	like_list = movie.like_list.all()
	dislike_list = movie.dislike_list.all()
	for user in like_list:
		vector[user.id - 1] = 1
	for user in dislike_list:
		vector[user.id - 1] = -1

	vector_str = ','.join(['%d' % num for num in vector])

	movie.vector = vector_str
	movie.save()

@transaction.atomic
def admin_save_movie(movie_id):
	# Fetch an existing movie or create a new object
	try:
		m_to_add = Movie.objects.get(imdb_id = movie_id)
	except Movie.DoesNotExist:
		i = imdb.IMDb()
		movie = i.get_movie(movie_id)

		m_to_add = Movie(imdb_id = movie_id, title = movie['title'], year = movie['year'])
		m_to_add.save()

		try:
			m_to_add.duration = movie['runtimes'][0] + ' min'
		except KeyError:
	    		pass

	    	# http://stackoverflow.com/questions/3042757/downloading-a-picture-via-urllib-and-python
		try:
		    	os.chdir(settings.MEDIA_ROOT + '/movie-covers/')  # set where files download to

			fileName=str('tt' + movie_id + ".jpg")  # string containing the file name
			if not os.path.isfile(fileName):
				url = movie['full-size cover url']
				url = url[:-3] + '_V1_SX214_AL_.jpg'

				urllib.urlretrieve(url, fileName) # uses the function defined above to download the pic

			m_to_add.cover = settings.MEDIA_URL + 'movie-covers/' + fileName
		except KeyError:
	    		pass
		
	    	try:
			director_list = movie['director']
			for d in director_list:
				try:
					director = Person.objects.get(person_id = d.personID)
					m_to_add.director_list.add(director)
				except Person.DoesNotExist:
					# new_director = Person(person_id = d.personID, name = d['name'])
					# new_director.save()
					m_to_add.director_list.add(admin_save_person(d.personID))
		except KeyError:
	    		pass

	    	try:
			producer_list = movie['producer']
			for pd in producer_list:
				try:
					producer = Person.objects.get(person_id = pd.personID)
					m_to_add.producer_list.add(producer)
				except Person.DoesNotExist:
					# new_producer = Person(person_id = pd.personID, name = pd['name'])
					# new_producer.save()
					m_to_add.producer_list.add(admin_save_person(pd.personID))
		except KeyError:
	    		pass

	    	try:
			writer_list = movie['writer']
			for w in writer_list:
				try:
					writer = Person.objects.get(person_id = w.personID)
					m_to_add.writer_list.add(writer)
				except Person.DoesNotExist:
					# new_writer = Person(person_id = w.personID, name = w['name'])
					# new_writer.save()
					m_to_add.writer_list.add(admin_save_person(w.personID))
		except KeyError:
	    		pass

	    	try:
			m_to_add.storyline = movie['plot'][0]
			m_to_add.short_storyline = movie['plot'][-1]
		except KeyError:
	    		pass

	    	try:
			cast_list = movie['cast']
			for s in cast_list:
				try:
					star = Person.objects.get(person_id = s.personID)
					m_to_add.cast_list.add(star)
				except Person.DoesNotExist:
					# new_star = Person(person_id = s.personID, name = s['name'])
					# new_star.save()
					m_to_add.cast_list.add(admin_save_person(s.personID))
				try:
					new_character = Character(name = s.currentRole['name'])
					new_character.save()
					m_to_add.character_list.add(new_character)
				except TypeError:
					c_name = ''
					for c in s.currentRole:
						c_name += c['name']
						c_name += ' / '
					c_name = c_name[:-3]
					new_character = Character(name = c_name)
					new_character.save()
					m_to_add.character_list.add(new_character)
		except KeyError:
	    		pass

	    	try:
			genre_list = movie['genres']
			for g in genre_list:
				try:
					genre = Genre.objects.get(name = g)
					m_to_add.genre_list.add(genre)
				except Genre.DoesNotExist:
					new_genre = Genre(name = g)
					new_genre.save()
					m_to_add.genre_list.add(new_genre)
		except KeyError:
	    		pass

	    	try:
			certificates = movie['certificates']
			last_usa_cer = [cer for cer in certificates if 'USA' in cer]
			if last_usa_cer:
				last_usa_cer = last_usa_cer[-1]
				index_first_colon = last_usa_cer.find(':') + 1
				index_second_colon = last_usa_cer.replace(':', '?', 1).find(':')
				c = last_usa_cer[index_first_colon:index_second_colon]
				m_to_add.certificate = c
			else:
				m_to_add.certificate = last_usa_cer
		except KeyError:
	    		pass

	    	m_to_add.ticket_url = get_fandango_url(movie['title'], movie_id)

	    	m_to_add.save()
    		print 'Movie ' + movie_id + ': ' + m_to_add.title + ' is added.'

	# Update the vector
	update_vector_all(m_to_add)
	# Update the user_vector
	users_all = User.objects.all()
	for u in users_all:
		s = smart_bytes(u.profile.user_vector, encoding='utf-8', strings_only=False, errors='strict')
		s += ',0'
		u.profile.user_vector = s
		u.profile.save()

	return m_to_add

def admin_add_movie(request, movie_id):
	context = {}
	m_to_add = admin_save_movie(movie_id)
	# Fill in the context
	context['imdb_id'] = m_to_add.imdb_id
	context['title'] = m_to_add.title
	context['year'] = m_to_add.year
	context['duration'] = m_to_add.duration
	context['cover'] = m_to_add.cover
	context['director'] = m_to_add.director_list.all()
	context['producer'] = m_to_add.producer_list.all()
	context['writer'] = m_to_add.writer_list.all()
	context['storyline'] = m_to_add.storyline
	context['short_storyline'] = m_to_add.short_storyline
	context['cast'] = m_to_add.cast_list.all()[:15]
	context['genres'] = m_to_add.genre_list.all()
	context['certificate'] = m_to_add.certificate

	return render(request, 'admin_movie.html', context)

@transaction.atomic
def admin_save_person(person_id):
	# Fetch an existing person or create a new person object
	try:
		p_to_add = Person.objects.get(person_id = person_id)
	except Person.DoesNotExist:
		p_to_add = Person(person_id = person_id)
		
	# If this is only an person object with incomplete info, update info
	if not p_to_add.has_full_info:
		i = imdb.IMDb()
		person = i.get_person(person_id)

		p_to_add.name = person['name']

		try:
			p_to_add.birthyear = person['birth date']
		except KeyError:
	    		pass

		try:
			p_to_add.birthnotes = person['birth notes']
		except KeyError:
	    		pass

		try:
			p_to_add.bio = person['mini biography'][0]
		except KeyError:
	    		pass

		try:
		    	os.chdir(settings.MEDIA_ROOT + '/person-photos/')  # set where files download to
			
			fileName=str('nm' + person_id + ".jpg")  # string containing the file name
			if not os.path.isfile(fileName):
				url = person['headshot']
				urllib.urlretrieve(url, fileName) # uses the function defined above to download the pic

			p_to_add.photo = settings.MEDIA_URL + 'person-photos/' + fileName
		except KeyError:
	    		pass

	    	p_to_add.has_full_info = True
	    	p_to_add.save()
	    	print 'Person ' + person_id + ': ' + p_to_add.name + ' is fully added.'
	
	return p_to_add

def admin_add_person(request, person_id):
	context = {}
	p_to_add = admin_save_person(person_id)
	# Fill in the context
	context['person_id'] = p_to_add.person_id
	context['name'] = p_to_add.name
	context['birthyear'] = p_to_add.birthyear
	context['birthnotes'] = p_to_add.birthnotes
	context['bio'] = p_to_add.bio
	context['photo'] = p_to_add.photo

	return render(request, 'admin_person.html', context)

def admin_one_touch(request):
	movie_list = [		 
			'1951265', # In theater
			'0816692', 
			'2015381', 
			'2170439',
			'2096672',
			'2245084',
			'2980516',
			'2713180', 
			'2267998', 
			'1911658',	

			'1791528', # Upcoming 1
			'1528100',
			'2784678',
			'2298394',

			'2310332', # Upcoming 2
			'1823664',
			'2692250',
			'2039393',
			'2473794',
			'2437548',

			'2180411', # Upcoming 3
			'1809398',
			'2788710',
			'2179136',
			'1126590',
			'2737050',
			'2790236',
			]
	for movie_id in movie_list:
		admin_save_movie(movie_id)
	print '--------------------One-touch is wonderful--------------------'
	return redirect('admin_homepage')
