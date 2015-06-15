 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash


@app.route('/')
def index():


	'''
		Hvis brugeren er logget ind, hvis forside
		Ellers hvis "spalshpage", hvor man kan oprette bruger og logge ind

	'''
	if g.userIsloggedIn == True:
		return render_template('pages/forside.jinja')
	else: 
		return render_template('pages/splashpage.jinja')

