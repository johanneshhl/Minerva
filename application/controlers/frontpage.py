 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash



@app.route('/')
def index():
	app.logger.debug('test')
	return '<h1>{0}</h1>'.format(app.config['APPLICATION_NAME'])