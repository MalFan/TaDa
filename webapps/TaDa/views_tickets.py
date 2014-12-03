import urllib2 
from HTMLParser import HTMLParser
# -*- coding: UTF-8 -*-

url_fandango = ''
class MyHTMLParserForUrl(HTMLParser):

  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0 
    self.data = []
  
  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for name, value in attrs:        
        if name == 'href' and value.startswith('http://www.fandango.com/redirect.aspx'):
          global url_fandango
          url_fandango = value
          return

def get_fandango_url(imdb_name, imdb_id):
	global url_fandango
	url_fandango = ''
	fandango_name = get_fandango_name(imdb_name)
	fandango_id = get_fandango_id(imdb_id)
	fandango_url = combine(fandango_name, fandango_id)
	return fandango_url

def get_fandango_name(imdb_name):
	imdb_name = imdb_name.lower()
	fandango_name = ""
	for c in imdb_name:
		if c.isalpha() or c.isdigit() or c == ':' or c == '.':
			fandango_name += c
	return fandango_name

def get_fandango_id(imdb_id):
	imdb_url_firstpart = 'http://www.imdb.com/showtimes/title/tt'
	imdb_url = imdb_url_firstpart + imdb_id
	
	p = MyHTMLParserForUrl()
	f_imdb = urllib2.urlopen(imdb_url)

	html_imdb = f_imdb.read()
	p.feed(html_imdb)
	start = url_fandango.find('mid') + 4
	end = url_fandango.find('mid') + 10

	fandango_id =  url_fandango[start:end]

	return fandango_id

def combine(fandango_name, fandango_id):
	if not fandango_id:
		return ''
	first_part = 'http://www.fandango.com/'
	second_part = '_'
	third_part = '/movietimes'
	fandango_url = first_part + fandango_name + second_part + fandango_id + third_part
	return fandango_url

