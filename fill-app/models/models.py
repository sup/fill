
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
    bio = ndb.TextProperty()
    education = ndb.TextProperty()
    skills = ndb.TextProperty()
    interests = ndb.TextProperty()
    profile_pic = ndb.StringProperty(default="http://www.homepcpatrol.com/sites/default/files/imagecache/Profile_Full/alice-stilwell.jpg")

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

    @classmethod
    def get_user_by_id(self, id):
        """Get an event by its key id"""
        return self.get_by_id(int(id))

class Event(ndb.Model):
    """
    Event model for the FILL app.
    """
    # Basic Info
    name = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(required=True)
    admin = ndb.KeyProperty(required=True)
    location = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    language = ndb.StringProperty(required=True)
    accessibility = ndb.StringProperty(required=True)
    hours = ndb.IntegerProperty(required=True)
    physical_activity = ndb.StringProperty(required=True)

    # Needed Personnel (Integers)
    volunteers_needed = ndb.IntegerProperty()
    drivers_needed = ndb.IntegerProperty()
    translators_needed = ndb.IntegerProperty()

    # Requests (List of Users)
    volunteer_requests = ndb.KeyProperty(repeated=True)
    driver_requests = ndb.KeyProperty(repeated=True)
    translator_requests = ndb.KeyProperty(repeated=True)

    # Accepted Personnel (List of Users)
    volunteers = ndb.KeyProperty(repeated=True)
    drivers = ndb.KeyProperty(repeated=True)
    translators = ndb.KeyProperty(repeated=True)

    # Instance methods for getting progress bar ratios
    def volunteer_fill_percentage(self):
        return int(float(len(self.volunteers))/self.volunteers_needed*100)

    def driver_fill_percentage(self):
        return int(float(len(self.drivers))/self.drivers_needed*100)

    def translator_fill_percentage(self):
        return int(float(len(self.translators))/self.translators_needed*100)


    def verify(self):
        # Fix some event values that are broken ... deprecated
        if self.volunteers_needed == [None]:
            self.volunteers_needed = []
        if self.drivers_needed == [None]:
            self.drivers_needed = []
        if self.translators_needed == [None]:
            self.translators_needed = []
        if self.volunteer_requests == [None]:
            self.volunteer_requests = []
        if self.driver_requests == [None]:
            self.driver_requests = []
        if self.translator_requests == [None]:
            self.translator_requests = []
        if self.volunteers == [None]:
            self.volunteers = []
        if self.drivers == [None]:
            self.drivers = []
        if self.translators == [None]:
            self.translators = []


    # Public API
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
        return self.query(Event.volunteers.IN([user]) or Event.drivers.IN([user]) or Event.translators.IN([user])).fetch()

    @classmethod
    def get_events_by_request(self, user):
        """Get a list of events by a user"""
        return self.query(Event.volunteer_requests.IN([user]) or Event.driver_requests.IN([user]) or Event.translator_requests.IN([user])).fetch()

    @classmethod
    def get_event_by_id(self, id):
        """Get an event by its key id"""
        return self.get_by_id(int(id))

class Post(ndb.Model):
    """
    Post model for the FILL app.
    """
    # Basic Info
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    writer = ndb.KeyProperty(required=True)

    # Public API
    @classmethod
    def get_posts_by_writer(self, user):
        """Get a list of posts by a user"""
        return self.query(self.writer == user).fetch()

    @classmethod
    def get_post_by_id(self, id):
        """Get a post by its key id"""
        return self.get_by_id(int(id))


# Debug
if __name__ == '__main__':
    pass