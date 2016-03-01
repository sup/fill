"""
event.py

Event model for the FILL app.
"""
from google.appengine.ext import ndb

class Event(ndb.Model):
	# Properties
	name = ndb.StringProperty(required=True)
	date = ndb.DateTimeProperty(required=True)
	admin = ndb.StringProperty(required=True)
	volunteers = ndb.StringProperty(repeated=True)
	description = ndb.TextProperty()

# Debug
if __name__ == '__main__':
	pass