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
from models.models import User, Event

# Template Directories
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

"""
Main View Controllers
"""
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
    # else: return render_template('dashboard.html', args*, kwargs**)

# TODO: Signup
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

# TODO: Login Controller
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

# Profile Controller
@app.route('/timeline')
def timeline():
    """Return Profile Page"""
    username = request.cookies.get('username')
    user = User.get_user(username)
    if user:
        joined_events = Event.get_events_by_volunteer(user.key)
        created_events = Event.get_events_by_admin(user.key)
        first_name = user.name.split(" ")[0]
        return render_template('timeline.html', user=user, first_name=first_name, joined_events=joined_events, created_events=created_events)
    else:
        return render_template('home.html', page_title="FILL")

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

# TODO: Event Feed Controller
@app.route('/events')
def events():
    """Return event feed"""
    events = Event.query().fetch()
    return render_template('event_feed.html', events=events)

@app.route('/event_page/')
@app.route('/event_page/<id>')
def event_page(id=None):
    """Return event page"""
    if id is None:
        return redirect(url_for('timeline'))
    event = Event.get_event_by_id(id)
    return render_template('event_page.html', event=event)

# TODO: Create Events Controller
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

@app.route('/edit_event/')
@app.route('/edit_event/<id>', methods=['GET', 'POST'])
def edit_event(id=None):
    """Edit Event Form"""
    if id is None:
        return redirect(url_for('admin'))
    pass

@app.route('/join_event/')
@app.route('/join_event/<id>', methods=['GET', 'POST'])
def join_event(id=None):
    if id is None:
        return redirect(url_for('events'))
    # Get user
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
        if volunteer and user.key not in event.volunteer_requests:
            event.volunteer_requests.append(user.key)
        if driver and user.key not in event.driver_requests:
            event.driver_requests.append(user.key)
        if translator and user.ey not in event.translator_requests:
            event.translator_requests.append(user.key)
        # Make sure the event makes sense - Probably deprecated
        event.verify()
        event.put()
        return render_template('join_event.html', event=event, success="Request successfully sent!")

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
