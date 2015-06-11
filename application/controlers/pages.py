 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from application import app, request, redirect, escape, session, abort, url_for, db, bcrypt, render_template, g, flash
from application.controlers.decorators import *
from application.database.database import Document, User, Product, Statistic




@app.route('/')
def index():

	if g.userIsloggedIn == True:
		return render_template('pages/forside.jinja')
	else: 
		return render_template('pages/splashpage.jinja')


@app.route('/create_document', methods=['GET'])
@login_required
def createDocument():
	return render_template('pages/createDocument.jinja')




@app.route('/view_document/<int:fileId>', methods=['GET'])
def viewDocument(fileId):

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

	return render_template('pages/displayDocuments.jinja', theDocuments=Document.query.filter_by(user_id=g.userId).order_by(Document.created.desc()))





@app.route('/public_view_documents/<int:fileId>', methods=['GET'])
def publicViewDocument(fileId):

	document = Document.query.filter_by(id=fileId).first()
	user = User.query.filter_by(id=document.user_id).first()

	if document != None:
		return render_template('pages/publicViewDocument.jinja', theUser=user, theDocument=document)

	else:
		abort(404)











@app.route('/login', methods=['GET'])
def login():
	return redirect(url_for('logUserIn'))



@app.route('/logoff', methods=['GET'])
@login_required
def logoff():
	return redirect(url_for('logUserOut'))







