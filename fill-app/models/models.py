
from google.appengine.ext import ndb

class User(ndb.Model):
    """
    User model for the FILL app.
    """
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
        """Check if a username is available to claim"""
        return self.query(self.username == username).count() is 0

    @classmethod
    def is_email_available(self, email):
        """Check if an email is available to claim"""
        return self.query(self.email == email).count() is 0

    @classmethod
    def get_user(self, username):
        """Return the first user matching a username query"""
        userlist = self.query(self.username == username).fetch(1)
        if len(userlist) == 0:
            return None
        else:
            return userlist[0]

    @classmethod
    def get_users(self, username):
        """Return a list of users matching a query"""
        userlist = self.query(self.username == username).fetch(1)
        if len(userlist) == 0:
            return None
        else:
            return userlist

class Event(ndb.Model):
    """
    Event model for the FILL app.
    """
    # Properties
    name = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)
    admin = ndb.StringProperty(required=True)
    volunteers = ndb.StringProperty(repeated=True)
    description = ndb.TextProperty(required=True)
    language = ndb.StringProperty(required=True)
    hours = ndb.IntegerProperty(required=True)
    physical_activity = ndb.StringProperty(required=True)
    volunteers_needed = ndb.IntegerProperty(required=True)
    drivered_needed = ndb.IntegerProperty(required=True)
    translators_needed = ndb.IntegerProperty(required=True)

    @classmethod
    def get_events(self, query_dict):
        """Get a list of events matching a query"""
        userlist = self.query(self.name == query_dict).fetch(1)
        if len(userlist) == 0:
            return None
        else:
            return userlist[0]

# Debug
if __name__ == '__main__':
    pass