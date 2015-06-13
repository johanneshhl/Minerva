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

	utf_Test = (u''+userDict['utf8']) == u'✓'
 	email_unic = (User.query.filter(User.email.ilike(userDict['email'])).first() == None)
 	password_long = (len(userDict['password']) >= 8)

	if (utf_Test and email_unic and password_long):
	
		#opret User opjectet med userDict og hashed kodeord
		newUser = User(userDict['firstname'], userDict['lastname'], userDict['email'], userDict['password'])
		
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

	user = User.query.filter(User.email.ilike(userDict['email'])).first()

	if user and bcrypt.check_password_hash(user.password, userDict['password']):
		loginUser(user)

		return redirect(returnURL)

	else:
		return render_login_user('Email eller kodeord er forkert')




def loginUser(userObj):

	userId = userObj.id
	userEmail = userObj.email
	userFirstname = userObj.firstname
	userLastName = userObj.lastname

	User.query.filter_by(email=userEmail).first().lastLogin = datetime.datetime.now()
	db.session.commit()

	session['email'] = userEmail
	session['userID'] = userId
	session['firstname'] = userFirstname
	session['lastname'] = userLastName
	
	session['LoggedIn'] = True

	session.permanent = True











