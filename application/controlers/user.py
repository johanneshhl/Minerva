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
		Hvis allrede loggedet ind send til forsiden (/)

		(GET)	Hvis opret bruger side
		(POST)	Lave ny bruger fra form


	'''

	if 'next' in request.args:
		returnURL = request.args['next']
	else:
		returnURL = url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME'])


	if (request.method == 'GET'):
		return render_create_user()

	if (request.method == 'POST'):
		return createUserFromDict(returnURL, request.form)





@app.route('/session/checkuser', methods=['POST'])
def checkuser():

	'''
		Funktion til at tjekke om at brugernavenet findes

	'''
	theUsername = request.form['email']
 	email_unic = (User.query.filter(User.email.ilike(theUsername)).first() == None)

	if theUsername == False or theUsername == '':
		return 'false', 400
	elif theUsername != '' and email_unic == True:
		return 'ok', 200
	else:
		return 'Username unavailable'






@app.route('/session/login', methods=['POST','GET'])
@allready_logged_in
def logUserIn():

	'''
		Log brugeren ind

		(GET)	Hvis Login bruger side
		(POST)	Login fra form


	'''

	if 'next' in request.args:
		returnURL = request.args['next']
	else:
		returnURL = url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME'])


	if (request.method == 'GET'):
		return render_login_user()

	if (request.method == 'POST'):
		return loginUserFromDict(returnURL, request.form)




@app.route('/login', methods=['GET'])
def login():
	'''
		Gammle function skal slettes
	'''

	return redirect(url_for('logUserIn', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))



@app.route('/logoff', methods=['GET'])
@login_required
def logoff():

	'''
		Log brugeren af og send til forsiden

	'''


	session.clear()
	flash('Logget af', 'info')

	return redirect(url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))


