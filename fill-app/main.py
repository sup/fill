# -*- coding: utf-8 -*-
"""
`main` is the top level module for your Flask application.
"""
import jinja2
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
app = Flask(__name__)
# Import custom libraries
from security import *
from models.event_model import *
from models.user_model import * 

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
    # if loggedin:
    return render_template('home.html', page_title="FILL")
    # else: return render_template('dashboard.html', args*, kwargs**)

# TODO: Login Controller
@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

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
        
        # Add the user
        available = User.is_username_available(username)
        if not available:
            return "That user exists"
        else:
            hashed_pw = make_pw_hash(str(username), str(password))
            user = User(name=name, 
                        username=username, 
                        email=email, 
                        password_hash=hashed_pw)
            user.put()
            response = make_response("Hello " + username)
            response.set_cookie('username', username)
            return response


# TODO: Create Event Controller

# TODO: Join Event Controller

# TODO: Show Events Controller
@app.route('/events')
def events():
	"""Return event feed"""
	return render_template('feed.html', page_title="Event Feed", events=[1,2,3])


"""
RESTful API for accessing NDB+Backend: search, etc -> useful with jQuery AJAX
"""
# TODO: Backend helper methods

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
