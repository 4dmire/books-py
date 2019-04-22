from yattag import Doc
from yattag import indent
from calendar import month_name
from lxml import etree, html
import json
import os

INDEX = 'index.html'
BOOK_JSON = 'books.json'
TWITTER = 'http://twitter.com/stayingpeachy_'
TWITCH = 'http://twitch.com/stayingpeachy'
GITHUB = 'https://github.com/stayingpeachy'

BOOTSTRAP_META = '''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'''
BOOTSTRAP_CSS = '''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'''
BOOTSTRAP_JS = '''<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>'''

MY_CSS = '<link href="style.css" rel="stylesheet">'

COLOR_MAP = {5: 'pink', 4: 'purple', 3: 'blue', 2: 'mint', 1: 'green'}
RATING = '!@#$%'

class Book:
	
	books = []
	
	def __init__(self, data):
		self.id = data['id']
		self.title = data['title']
		self.author = data['author']
		self.rating = data['rating']
		self.books.append(self)
	
	def __str__(self):
		
		return '{} by {} - {}'.format(self.title, self.author, RATING[:self.rating])
		
	def get_color(self):
		return COLOR_MAP[self.rating]
	

def load_data():
	source = BOOK_JSON
	with open(source) as data:
		book_json = json.load(data)
		for d in book_json:
			Book(d)


def build_html():
	doc, tag, text = Doc().tagtext()
	doc.asis('<!DOCTYPE html>')
	with tag('html'):
		with tag('head'):
			doc.asis(BOOTSTRAP_META)
			doc.asis(BOOTSTRAP_CSS)
			doc.asis(MY_CSS)
			with tag('title'):
				text('redrover books')
		with tag('body'):
			with tag('div', klass='container main'):
				with tag('div', klass='row intro'):
					text('books redrover read')
				for book in Book.books:
					with tag('div', klass='row book {}'.format(book.get_color())):
						text(str(book))
				with tag('div', klass='row foot'):
					with tag('a', href=TWITTER, target='_blank'):
						text('twitter')
					text('/')
					with tag('a', href=TWITCH, target='_blank'):
						text('twitch')
					text('/')
					with tag('a', href=GITHUB, target='_blank'):
						text('github')
			doc.asis(BOOTSTRAP_JS)
	return doc.getvalue()


def write_file(doc):	
	if os.path.exists(INDEX):
		os.remove(INDEX)
	with open(INDEX, 'w') as f:
		f.write(indent(doc))
	
	
def main():
	load_data()
	doc = build_html()
	write_file(doc)
	
main()
