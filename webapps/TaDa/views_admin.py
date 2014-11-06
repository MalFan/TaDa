from django.shortcuts import render
import imdb

from models import *
# from forms import *

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


def admin_add_movie(request, movie_id):
	context = {}
	# Fetch an existing movie or create a new object
	try:
		m_to_add = Movie.objects.get(imdb_id = movie_id)
	except Movie.DoesNotExist:
		i = imdb.IMDb()
		movie = i.get_movie(movie_id)

		m_to_add = Movie(imdb_id = movie_id, title = movie['title'], year = movie['year'])
		m_to_add.save()

		try:
			m_to_add.cover = movie['cover url']
		except KeyError:
	    		pass
		
	    	try:
			director_list = movie['director']
			for d in director_list:
				try:
					director = Person.objects.get(person_id = d.personID)
					m_to_add.director_list.add(director)
				except Person.DoesNotExist:
					new_director = Person(person_id = d.personID, name = d['name'])
					new_director.save()
					m_to_add.director_list.add(new_director)
		except KeyError:
	    		pass

	    	try:
			writer_list = movie['writer']
			for w in writer_list:
				try:
					writer = Person.objects.get(person_id = w.personID)
					m_to_add.writer_list.add(writer)
				except Person.DoesNotExist:
					new_writer = Person(person_id = w.personID, name = w['name'])
					new_writer.save()
					m_to_add.writer_list.add(new_writer)
		except KeyError:
	    		pass

	    	try:
			m_to_add.storyline = movie['plot'][0]
		except KeyError:
	    		pass

	    	try:
			cast_list = movie['cast']
			for s in cast_list:
				try:
					star = Person.objects.get(person_id = s.personID)
					m_to_add.cast_list.add(star)
				except Person.DoesNotExist:
					new_star = Person(person_id = s.personID, name = s['name'])
					new_star.save()
					m_to_add.cast_list.add(new_star)
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
			last_usa_cer = [cer for cer in certificates if 'USA' in cer][-1]
			index_first_colon = last_usa_cer.find(':') + 1
			index_second_colon = last_usa_cer.replace(':', '?', 1).find(':')
			c = last_usa_cer[index_first_colon:index_second_colon]
			m_to_add.certificate = c
		except KeyError:
	    		pass

	    	m_to_add.save()

	# Fill in the context
	context['imdb_id'] = m_to_add.imdb_id
	context['title'] = m_to_add.title
	context['year'] = m_to_add.year
	context['cover'] = m_to_add.cover
	context['director'] = m_to_add.director_list.all()
	context['writer'] = m_to_add.writer_list.all()
	context['storyline'] = m_to_add.storyline
	context['cast'] = m_to_add.cast_list.all()[:15]
	context['genres'] = m_to_add.genre_list.all()
	context['certificate'] = m_to_add.certificate

	return render(request, 'admin_movie.html', context)


def admin_add_person(request, person_id):
	context = {}
	# Fetch an existing person or create a new person object
	try:
		p_to_add = Person.objects.get(person_id = person_id)
	except Person.DoesNotExist:
		p_to_add = Person(person_id = person_id)
		
	# If this is only an person object with incomplete info, update info
	if not p_to_add.has_full_info:
		i = imdb.IMDb()
		person = i.get_person(person_id)

		try:
			p_to_add.birthyear = person['birth date']
		except KeyError:
	    		pass

		try:
			p_to_add.bio = person['mini biography'][0]
		except KeyError:
	    		pass
		
		try:
			p_to_add.photo = person['headshot']
		except KeyError:
	    		pass

	    	p_to_add.has_full_info = True
	    	p_to_add.save()

	# Fill in the context
	context['person_id'] = p_to_add.person_id
	context['name'] = p_to_add.name
	context['birthyear'] = p_to_add.birthyear
	context['bio'] = p_to_add.bio
	context['photo'] = p_to_add.photo

	return render(request, 'admin_person.html', context)
