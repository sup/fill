# -*- coding: utf-8 -*-
"""
`main` is the top level module for your Flask application.
"""
import jinja2
import os
from flask import Flask
from flask import render_template
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

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
@app.route('/login')
def login():
	pass

# TODO: Signup
@app.route('/signup')
def signup():
	pass

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
