 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, abort, url_for, jsonify, db, bcrypt, render_template, g, flash
from application.controlers.decorators import *
from application.database.database import Document, User, Product, Statistic






@app.route('/search', methods=['get'])
@login_required
def searchWithParam():

	
	requestString = request.args.get('search_input')

	SearchResult = Document.query.filter(db.or_(
		Document.name.contains(requestString),
		Document.subtitle.contains(requestString),
		Document.description.contains(requestString),
		Document.subject.contains(requestString),
		Document.topic.contains(requestString),
		Document.education_level.contains(requestString)
		)).limit(20)


	result = {}
	x = 0

	#for newDocument in SearchResult:
	#	x += 1
	#	result.update(
	#			{'item{}'.format(x):
	#				{ 
	#					'name': newDocument.name,
	#				 	'subtitle':newDocument.subtitle,
	#				 	'description':newDocument.description,
	#				 	'subject':newDocument.subject,
	#				 	'topic':newDocument.topic,
	#				 	'education_level':newDocument.education_level
	#				 }
	#			}
	#		)

	#return jsonify(result)


	return render_template('pages/search.jinja', param=requestString, theDocuments=SearchResult, amount=SearchResult.count())


