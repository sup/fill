# -*- coding: utf-8 -*-
"""
`main` is the top level module for your Flask application.
"""
import jinja2
import os
from flask import Flask, render_template, request, make_response, redirect, url_for
from datetime import datetime, timedelta
app = Flask(__name__)
# Import custom libraries
from util.security import *
from models.models import User, Event, Post

# Template Directories
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

"""
No Cache Decorator
"""
from functools import wraps, update_wrapper
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

"""
Main View Controllers
"""
# Home Controller
@app.route('/')
def home():
    """Return landing page if not logged in, else show dashboard"""
    # TODO: Gatekeeper Controller
    username = request.cookies.get('username')
    user = User.get_user(username)
    if user:
        return redirect(url_for('timeline'))
    else:
        return render_template('home.html', page_title="FILL")

# Signup Controller
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # Display the Signup form
        return render_template('signup.html')
    else:
        # Signup the User
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # TODO: Verify user data
        available = User.is_username_available(username)
        if not available:
            return render_template('signup.html', error="User already exists!")
        else:
            # Add the user
            hashed_pw = make_pw_hash(str(username), str(password))
            user = User(name=name, 
                        username=username, 
                        email=email, 
                        password_hash=hashed_pw)
            user.put()
            response = make_response(redirect(url_for('home')))
            response.set_cookie("username", username)
            return response

# Login Controller
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # TODO: If logged in, redirect to dashboard
       return render_template('login.html')
    else:
        # Paarse the form
        username = request.form["username"]
        password = request.form["password"]
        # Get the User and check password
        user = User.get_user(username)
        if user is None:
            return render_template('login.html', error="User doesn't exist!")
        hashed_pw = user.password_hash
        if not valid_pw(username, password, hashed_pw):
            return render_template('login.html', error="Password incorrect!")
        else:
            response = make_response(redirect(url_for('timeline')))
            response.set_cookie("username", username)
            return response

# Logout Controller
@app.route('/logout')
def logout():
    response = make_response(render_template('login.html', success="Successfully logged out."))
    response.set_cookie('username', '')
    return response

"""
Timeline and Admin
"""
# Profile Controller
@app.route('/timeline')
@app.route('/timeline/<id>')
def timeline(id=None):
    """Return Profile Page"""
    # Hacky redirect - refactor in the future
    username = request.cookies.get('username')
    cookie_user = User.get_user(username)
    if not id:
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        user = User.get_user_by_id(id)
    if user:
        is_owner = cookie_user == user
        joined_events = Event.get_events_by_volunteer(user.key)
        created_events = Event.get_events_by_admin(user.key)
        posts = Post.get_posts_by_writer(user.key)
        first_name = user.name.split(" ")[0]
        return render_template('timeline.html', is_owner=is_owner, user=user, first_name=first_name, joined_events=joined_events, created_events=created_events, posts=posts)
    else:
        return render_template('home.html', page_title="FILL")

# Edit Timeline Controller
@app.route('/edit_timeline')
@app.route('/edit_timeline/<id>', methods=['GET', 'POST'])
def edit_timeline(id=None):
    """Edit Timeline Info"""
    # Hacky redirect - refactor in the future
    username = request.cookies.get('username')
    cookie_user = User.get_user(username)
    if request.method == "GET":
        return redirect('timeline/' + str(cookie_user.key.id()))
    if not id:
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        user = User.get_user_by_id(id)
    if user == cookie_user and request.method == "POST":
        user.bio = request.form.get("bio")
        user.skills = request.form.get("skills")
        user.interests = request.form.get("interests")
        user.put()
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        return redirect('timeline/' + str(cookie_user.key.id()))

# Create Post Controller
@app.route('/create_post')
@app.route('/create_post/<id>', methods=['GET', 'POST'])
def create_post(id=None):
    """Create a Post"""
    # Hacky redirect - refactor in the future
    username = request.cookies.get('username')
    cookie_user = User.get_user(username)
    if request.method == "GET":
        return redirect('timeline/' + str(cookie_user.key.id()))
    if not id:
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        user = User.get_user_by_id(id)
    if user == cookie_user and request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        # Create a Post
        post = Post(title=title, body=body, writer=user.key)
        post.put()
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        return redirect('timeline/' + str(cookie_user.key.id()))

# Edit Post Controller
@app.route('/edit_post')
@app.route('/edit_post/<id>/<post_id>', methods=['GET', 'POST'])
def edit_post(id=None, post_id=None):
    """Edit a Post"""
    # Hacky redirect - refactor in the future
    username = request.cookies.get('username')
    cookie_user = User.get_user(username)
    if request.method == "GET":
        return redirect('timeline/' + str(cookie_user.key.id()))
    if not id or not post_id:
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        user = User.get_user_by_id(id)
    if user == cookie_user and request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        post = Post.get_post_by_id(post_id)
        post.title = title
        post.body = body
        # Create a Post
        post.put()
        return redirect('timeline/' + str(cookie_user.key.id()))
    else:
        return redirect('timeline/' + str(cookie_user.key.id()))

@app.route('/delete_post/')
@app.route('/delete_post/<id>')
def delete_post(id=None):
    # Check user
    username = request.cookies.get('username')
    user = User.get_user(username)
    if not user:
        return redirect(url_for('home'))
    # Check id 
    if id is None:
        return redirect('timeline/' + str(user.key.id()))
    # Check Post
    post = Post.get_post_by_id(id)
    if not post:
        return redirect('timeline/' + str(user.key.id()))
    if post.writer.id() != user.key.id():
        return redirect('timeline/' + str(user.key.id()))

    # Delete the event
    post.key.delete()
    return redirect('timeline/' + str(user.key.id()))

# Admin Controller
@app.route('/admin')
def admin():
    """Return Admin Page"""
    username = request.cookies.get('username')
    user = User.get_user(username)
    if user:
        joined_events = Event.get_events_by_volunteer(user.key)
        created_events = Event.get_events_by_admin(user.key)
        requested_events = Event.get_events_by_request(user.key)
        return render_template('admin.html', user=user, joined_events=joined_events, created_events=created_events, requested_events=requested_events)
    else:
        return render_template('home.html', page_title="FILL")

"""
Event Controllers
"""
@app.route('/events')
def events():
    """Return event feed"""
    events = Event.query().fetch()
    return render_template('event_feed.html', events=events)

# Event Page Controller
@app.route('/event_page/')
@app.route('/event_page/<id>')
def event_page(id=None):
    """Return event page"""
    if id is None:
        return redirect(url_for('timeline'))
    event = Event.get_event_by_id(id)
    return render_template('event_page.html', event=event)

# Create Events Controller
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """Create Event Form"""
    if request.method == 'GET':
        return render_template('create_event.html')
    else:
        # Parse the form
        name = request.form["name"]
        date = request.form["date"]
        date = datetime.strptime(date, "%m/%d/%Y %H:%M %p")
        hours = int(request.form["hours"])
        description = request.form["description"]
        language = request.form["language"]
        physical_activity = request.form["physical_activity"]
        volunteers_needed = int(request.form["volunteers_needed"])
        drivers_needed = int(request.form["drivers_needed"])
        translators_needed = int(request.form["translators_needed"])

        # Get admin
        username = request.cookies.get('username')
        user = User.get_user(username)

        # Create and event
        event = Event(name=name, 
                      date=date, 
                      hours=hours, 
                      description=description,
                      language=language,
                      physical_activity=physical_activity,
                      volunteers_needed=volunteers_needed,
                      drivers_needed=drivers_needed,
                      translators_needed=translators_needed,
                      admin=user.key)
        event.put()

        return render_template('create_event.html', success="Event successfully created!")

# Edit Event Controller
@app.route('/edit_event/')
@app.route('/edit_event/<id>', methods=['GET', 'POST'])
def edit_event(id=None):
    """Edit Event Form"""
    # Check ID
    if id is None:
        return redirect(url_for('admin'))
    # Get user
    username = request.cookies.get('username')
    user = User.get_user(username)
    if not user:
        return redirect(url_for('home'))
    # Get Event
    event = Event.get_event_by_id(id)
    if event.admin.id() != user.key.id():
        return redirect(url_for('admin'))

    # Handle Requests
    if request.method == 'GET':
        return render_template('edit_event.html', event=event)
    else:
        # Parse the form
        name = request.form["name"]
        date = request.form["date"]
        date = datetime.strptime(date, "%m/%d/%Y %H:%M %p")
        hours = int(request.form["hours"])
        description = request.form["description"]
        language = request.form["language"]
        physical_activity = request.form["physical_activity"]
        volunteers_needed = int(request.form["volunteers_needed"])
        drivers_needed = int(request.form["drivers_needed"])
        translators_needed = int(request.form["translators_needed"])

        # Update the event
        event.name = name
        event.date = date
        event.hours = hours
        event.description = description
        event.language = language
        event.physical_activity = physical_activity
        event.volunteers_needed = int(volunteers_needed)
        event.drivers_needed = int(drivers_needed)
        event.translators_needed = int(translators_needed)
        event.put()

        # Return success message
        return render_template('edit_event.html', event=event, success="Event successfully edited!")

@app.route('/delete_event/')
@app.route('/delete_event/<id>')
def delete_event(id=None):
    # Check id 
    if id is None:
        return redirect(url_for('admin'))
    # Check user
    username = request.cookies.get('username')
    user = User.get_user(username)
    if not user:
        return redirect(url_for('home'))
    # Check Event
    event = Event.get_event_by_id(id)
    if not event:
        return redirect(url_for('admin'))
    if event.admin.id() != user.key.id():
        return redirect(url_for('admin'))

    # Delete the event
    event.key.delete()
    return render_template('admin.html', success="Event successfully deleted.")

# Join Event Controller
@app.route('/join_event/')
@app.route('/join_event/<id>', methods=['GET', 'POST'])
def join_event(id=None):
    # Check event id exists
    if id is None:
        return redirect(url_for('events'))
    # Get user and event
    username = request.cookies.get('username')
    user = User.get_user(username)
    event = Event.get_event_by_id(id)

    # Show form or process join as query
    if request.method == 'GET':
        volunteer = request.args.get("volunteer")
        driver = request.args.get("driver")
        translator = request.args.get("translator")
        return render_template('join_event.html', event=event, volunteer=volunteer, driver=driver, translator=translator)

    # Handle post data from form
    else:
        volunteer = request.form.get("volunteer")
        driver = request.form.get("driver")
        translator = request.form.get("translator")
        # Check uniqueness and append to NDB model
        error = None
        if volunteer:
            if user.key not in event.volunteer_requests and user.key not in event.volunteers:
                event.volunteer_requests.append(user.key)
            else:
                error = "You have already sent a request or are already a volunteer!"
        if driver:
            if user.key not in event.driver_requests and user.key not in event.drivers:
                event.driver_requests.append(user.key)
            else:
                error = "You have already sent a request or are already a driver!"
        if translator:
            if user.key not in event.translator_requests and user.key not in event.translators:
                event.translator_requests.append(user.key)
            else: 
                error = "You have already sent a request or are already a translator!"
        if error:
            return render_template('join_event.html', event=event, error=error)
        # Make sure the event makes sense - Probably deprecated
        event.verify()
        event.put()
        return render_template('join_event.html', event=event, success="Request successfully sent!")

# Check Request Controller
@app.route('/check_requests/')
@app.route('/check_requests/<id>', methods=['GET', 'POST'])
def check_requests(id=None):
    # Check ID
    if id is None:
        return redirect(url_for('admin'))

    # Get user
    username = request.cookies.get('username')
    user = User.get_user(username)
    if not user:
        return redirect(url_for('home'))

    # Get Event
    event = Event.get_event_by_id(id)

    # Handle Render Form Template
    if request.method == 'GET' and event.admin.id() == user.key.id():
        # Check for GET Parameters
        user_id = request.args.get("user")
        if not user_id:
            return render_template('check_requests.html', event=event)
        user = User.get_user_by_id(user_id)
        volunteer = request.args.get("volunteer")
        driver = request.args.get("driver")
        translator = request.args.get("translator")
        accept = int(request.args.get("accept"))
        # Accept the User
        if accept:
            if volunteer:
                event.volunteer_requests = [x for x in event.volunteer_requests if x != user.key]
                event.volunteers.append(user.key)
            if driver:
                event.driver_requests = [x for x in event.driver_requests if x != user.key]
                event.drivers.append(user.key)
            if translator:
                event.translator_requests = [x for x in event.translator_requests if x != user.key]
                event.translators.append(user.key)
            event.put()
            return render_template('check_requests.html', event=event, success="User successfully accepted!")
        # Reject the User
        else:
            if volunteer:
                event.volunteer_requests = [x for x in event.volunteer_requests if x != user.key]
            if driver:
                event.driver_requests = [x for x in event.driver_requests if x != user.key]
            if translator:
                event.translator_requests = [x for x in event.translator_requests if x != user.key]
            event.put()
            return render_template('check_requests.html', event=event, success="User successfully rejected.")
    else:
        return redirect(url_for('admin'))

"""
API
"""
# Application Health Controller
@app.route('/health')
def health():
    """Return OK if the app is working"""
    return "OK"

# Get Events JSON Controller
@app.route('/get_events', methods=['GET'])
def get_events():
    """Return a JSON object of event data for AJAX"""
    return "[]"

"""
Error Handlers
"""
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
