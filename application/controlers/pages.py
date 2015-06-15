 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, abort, url_for, db, bcrypt, render_template, g, flash
from application.controlers.decorators import *
from application.database.database import Document, User, Product, Statistic




@app.route('/create_document', methods=['GET'])
@login_required
def createDocument():

	'''
		Opret dokument side
		kræver login

	'''

	return render_template('pages/createDocument.jinja')




@app.route('/view_document/<int:fileId>', methods=['GET'])
def viewDocument(fileId):

	'''
		Vis dokument,
		hvis brugern er logget ind vis dokumentet
		ellers vis den offenlige dokument side

	'''

	if g.userIsloggedIn == True:

		document = Document.query.filter_by(id=fileId).first()
		if document != None:
			return render_template('pages/displayDocument.jinja', theDocument=document)
	
		else:
			abort(404)

	else:
		return redirect(url_for('publicViewDocument', fileId=fileId))



@app.route('/view_documents', methods=['GET'])
@login_required
def viewDocuments():

	'''

		Vis alle dokumenter lavet af "current" user 
		kræver login


	'''


	return render_template('pages/displayDocuments.jinja', theDocuments=Document.query.filter_by(user_id=g.userId).order_by(Document.created.desc()))





@app.route('/public_view_documents/<int:fileId>', methods=['GET'])
def publicViewDocument(fileId):

	'''

		Vis den offenlige dokument side

	'''


	document = Document.query.filter_by(id=fileId).first()
	user = User.query.filter_by(id=document.user_id).first()

	if document != None:
		return render_template('pages/publicViewDocument.jinja', theUser=user, theDocument=document)

	else:
		abort(404)













