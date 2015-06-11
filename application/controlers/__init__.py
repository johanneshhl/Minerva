 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash
from application.controlers import frontpage, user, decorators, document, pages
import datetime


@app.before_request
def before_request():
	g.year = datetime.datetime.now().year
	
	g.siteName = app.config['APPLICATION_NAME']
	g.siteOwner = app.config['APPLICATION_OWNER']
	g.siteVersion = app.config['APPLICATION_VERSION']

	g.baseUrl = url_for('index')

	if 'LoggedIn' in session:
		g.userIsloggedIn = True
	else:
		g.userIsloggedIn = False

	if g.userIsloggedIn:
		g.userId = session['userID']
		g.userFirstname = session['firstname']
		g.userLastName = session['lastname']

	