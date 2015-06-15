 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash
from application.database.database import User
import datetime




def render_create_user(message=None):
	if message != None:
		flash(message, 'error')

	return render_template('blocks/createUser.jinja')


def render_login_user(message=None):
	if message != None:
		flash(message, 'error')
	
	return render_template('pages/login.jinja')






def createUserFromDict(returnURL, userDict):

	'''
		Opret bruger fra Dict
		eller returer fejl


	'''
 
	utf_Test = (u''+userDict['utf8']) == u'✓' # er input utf-8 - bruges ikke endnu...

 	email_unic = (User.query.filter(User.email.ilike(userDict['email'])).first() == None) #Er email'en unik
 	
 	password_long = (len(userDict['password']) >= 8) # Er koden 8 eller over

	if (utf_Test and email_unic and password_long): #test af email_unic og kodeord 
	
		newUser = User(userDict['firstname'], userDict['lastname'], userDict['email'], userDict['password']) #opret bruger
		
		#indsæt User Objectet
		db.session.add(newUser)
		db.session.commit()

		#Log brugen ind
		loginUser(newUser)

		#returner Sandt
		return redirect(returnURL)

	else:
		return render_create_user('Kunne ikke oprette brugeren')



def loginUserFromDict(returnURL, userDict):

	'''
		Log brueren ind fra Dict

	'''

	user = User.query.filter(User.email.ilike(userDict['email'])).first() #find brugern hvor email er den samme som input email

	if user and bcrypt.check_password_hash(user.password, userDict['password']): #Er bruger ikke None &	passer brugern's hashed det den samme som input email
		#Log brugen ind
		loginUser(user)

		#send til "returnURL" normalt Forsiden
		return redirect(returnURL)

	else:
		return render_login_user('Email eller kodeord er forkert')




def loginUser(userObj):

	'''
		login bruger fra bruger Objekt

	'''

	userId = userObj.id
	userEmail = userObj.email
	userFirstname = userObj.firstname
	userLastName = userObj.lastname

	#opdater sidst logget in
	User.query.filter_by(email=userEmail).first().lastLogin = datetime.datetime.now()
	db.session.commit()


	#lav ny cryptedet cookie, aka. Flask.session

	session['email'] = userEmail
	session['userID'] = userId
	session['firstname'] = userFirstname
	session['lastname'] = userLastName
	
	session['LoggedIn'] = True

	#Husk mig - altid
	session.permanent = True











