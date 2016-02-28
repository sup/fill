"""
user.py

User model for the FILL app.
"""
from google.appengine.ext import ndb

class User(ndb.Model):
	# Properties
    username = ndb.StringProperty(required = True)
    password_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    created_events = ndb.StringProperty(repeated=True)
    joined_events = ndb.StringProperty(repeated=True)

# Debug
if __name__ == '__main__':
	pass