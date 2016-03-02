"""
user.py

User model for the FILL app.
"""
from google.appengine.ext import ndb

class User(ndb.Model):
    # User Properties
    name = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    password_hash = ndb.StringProperty(required = True)

    # Event Related Properties
    created_events = ndb.StringProperty(repeated=True)
    joined_events = ndb.StringProperty(repeated=True)

    @classmethod
    def is_username_available(self, username):
        return self.query(self.username == username).count() is 0

    @classmethod
    def is_email_available(self, email):
        return self.query(self.email == email).count() is 0

    @classmethod
    def get_user(self, username):
        userlist = self.query(self.username == username).fetch(1)
        if len(userlist) == 0:
            return None
        else:
            return userlist[0]

# Debug
if __name__ == '__main__':
    pass