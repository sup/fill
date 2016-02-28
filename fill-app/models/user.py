"""
user.py

User model for the FILL app.
"""
from google.appengine.ext import ndb

class User(ndb.Model):
	# Properties
    username = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = False)

# Debug
if __name__ == '__main__':
	pass