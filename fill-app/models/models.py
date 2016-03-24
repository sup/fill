
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
        userlist = self.query(self.username == username).fetch()
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
    admin = ndb.KeyProperty(required=True)
    volunteers = ndb.KeyProperty(repeated=True)
    description = ndb.TextProperty(required=True)
    language = ndb.StringProperty(required=True)
    hours = ndb.IntegerProperty(required=True)
    physical_activity = ndb.StringProperty(required=True)
    volunteers_needed = ndb.IntegerProperty(required=True)
    drivers_needed = ndb.IntegerProperty(required=True)
    translators_needed = ndb.IntegerProperty(required=True)

    @classmethod
    def get_events_by_name(self, name):
        """Get a list of events matching name"""
        return self.query(self.name == name).fetch()

    @classmethod
    def get_events_by_admin(self, user):
        """Get a list of events by a user"""
        return self.query(self.admin == user).fetch()


    @classmethod
    def get_events_by_volunteer(self, user):
        """Get a list of events by a user"""
        return self.query(Event.volunteers.IN([user])).fetch()

    @classmethod
    def get_event_by_id(self, id):
        """Get an event by its key id"""
        return self.get_by_id(int(id))


# Debug
if __name__ == '__main__':
    pass