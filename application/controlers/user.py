 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash
from application.models.user import *
from application.controlers.decorators import *
import application.database


@app.route('/session/create_user', methods=['POST','GET'])
@allready_logged_in
def createUser():

	'''

		create user site and api


	'''
	if 'next' in request.args:
		returnURL = request.args['next']
	else:
		returnURL = url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME'])


	if (request.method == 'GET'):
		return render_create_user()

	if (request.method == 'POST'):
		return createUserFromDict(returnURL, request.form)






@app.route('/session/login', methods=['POST','GET'])
@allready_logged_in
def logUserIn():

	'''

		create user site and api


	'''
	if 'next' in request.args:
		returnURL = request.args['next']
	else:
		returnURL = url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME'])


	if (request.method == 'GET'):
		return render_login_user()

	if (request.method == 'POST'):
		return loginUserFromDict(returnURL, request.form)





@app.route('/session/logout', methods=['GET'])
def logUserOut():

	session.clear()
	flash('Logget af', 'info')

	return redirect(url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))



	