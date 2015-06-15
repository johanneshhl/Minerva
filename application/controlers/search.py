 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, abort, url_for, jsonify, db, bcrypt, render_template, g, flash
from application.controlers.decorators import *
from application.database.database import Document, User, Product, Statistic






@app.route('/search', methods=['get'])
@login_required
def searchWithParam():


	'''

		Søg efter dokument ud fra meta data
		maksimal 20 svar

		og retuner side med svar

	'''
	
	requestString = request.args.get('search_input')
	parameters = requestString.split(" ",1)
	orParam = ''


 	search = ''
	for i in range(len(parameters)):
		if i == 0:
			SearchResult = Document.query.filter(db.or_(Document.name.ilike('%'+parameters[i]+'%'),
									Document.subtitle.ilike('%'+parameters[i]+'%'),
									Document.description.ilike('%'+parameters[i]+'%'),
									Document.subject.ilike('%'+parameters[i]+'%'),
									Document.topic.ilike('%'+parameters[i]+'%'),
									Document.education_level.ilike('%'+parameters[i]+'%'))).order_by(Document.created.desc())
		else:
			SearchResult.from_self().filter(db.or_(Document.name.ilike('%'+parameters[i]+'%'),
									Document.subtitle.ilike('%'+parameters[i]+'%'),
									Document.description.ilike('%'+parameters[i]+'%'),
									Document.subject.ilike('%'+parameters[i]+'%'),
									Document.topic.ilike('%'+parameters[i]+'%'),
									Document.education_level.ilike('%'+parameters[i]+'%'))).limit(20)

	return render_template('pages/search.jinja', param=requestString, theDocuments=SearchResult, amount=SearchResult.count())


