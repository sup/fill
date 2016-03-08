# -*- coding: utf-8 -*-
"""
`main` is the top level module for your Flask application.
"""
import jinja2
import os
from flask import Flask, render_template, request, make_response, redirect, url_for
app = Flask(__name__)
# Import custom libraries
from util.security import *
from models.models import User

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
        return render_template('dashboard.html', name=user.name)
    else:
        return render_template('profile.html', page_title="FILL")
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
        # Process the form
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
            response = make_response(redirect(url_for('profile')))
            response.set_cookie("username", username)
            return response

# Logout Controller
@app.route('/logout')
def logout():
    response = make_response(render_template('login.html', success="Successfully logged out."))
    response.set_cookie('username', '')
    return response

# Profile Controller
@app.route('/profile')
def profile():
    """Return Profile Page"""
    return render_template('profile.html')

# TODO: Event Feed Controller
@app.route('/events')
def events():
    """Return event feed"""
    return render_template('feed.html', events=[1,2,3])

# TODO: Create Events Controller
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """Create Event Form"""
    if request.method == 'GET':
        return render_template('create_event.html')
    else:
        pass

# Application Health Controller
@app.route('/health')
def health():
    """Return OK if the app is working"""
    return "OK"

"""
API for jQuery AJAX
"""
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
