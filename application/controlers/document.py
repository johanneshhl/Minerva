 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from application import app, abort, request, Response, redirect, escape, session, url_for, send_file, db, bcrypt, render_template, g, flash
from application.models.document import *
from application.controlers.decorators import *
from application.database.database import Document, Product, User
from io import BytesIO





@app.route('/session/get_document_info', methods=['POST'])
def testUpload():
	response = get_docx_info(request.files['file'])
	response.headers['Content-Type'] = 'text/html; charset=utf-8'
	return response


@app.route('/session/get_all_documents_from_user/<int:userId>', methods=['GET'])
def get_all_documents_from_user(userId):
	documents = Document.query.filter_by(user_id=userId).limit(20)
	user = User.query.filter_by(id=userId).first()
	return render_template('pages/displayDocumentsNotLoggedIn.jinja', theDocuments=documents, theUser=user)



@app.route('/session/upload_document', methods=['POST'])
@login_required
def uploadDocument():


	file = request.files['file']
	return Add_Docx_to_database(file, request.form)




@app.route('/session/update_document/<int:fileId>', methods=['GET', 'POST'])
@login_required
def update_document(fileId):

	if request.method == 'POST':
		
		return update_document_from_dict(fileId, request.form, request.files['file'])

	else:
		file = Document.query.filter_by(id=fileId).first()

		if file.user_id == int(g.userId):
			return render_template('pages/updateDocument.jinja', theDocument=file)
		else:
			abort(403)




@app.route('/session/document/download_epub/<int:fileId>', methods=['GET'])
def download_epub(fileId):

	if Document.query.filter_by(id=fileId).first() != None:
		
		epub = create_epub_from_id(fileId)
	
		epub_id = Product.query.filter_by(document_id=fileId, type='epub').first().id
		update_or_create_Statistic(epub_id, 'download')
	
		strIO = BytesIO(epub[0])
		filename = epub[1]+'.epub'
		return send_file(strIO, as_attachment=True, attachment_filename=filename, mimetype='application/epub+zip')

	else:
		abort(404)





@app.route('/session/document/show_html/<int:fileId>', methods=['GET'])
def html_view(fileId):

	if Document.query.filter_by(id=fileId).first() != None:

		HTML = create_HTML_from_id(fileId)
		document = Document.query.filter_by(id=fileId).first()
		user = User.query.filter_by(id=document.user_id).first()

		html_id = Product.query.filter_by(document_id=fileId, type='html').first().id
		update_or_create_Statistic(html_id, 'displays')
		
		return render_template('pages/documentWebsiteView.jinja', theDocument=document, theUser=user, content=HTML[0])

	else:
		abort(404)


@app.route('/session/document/original_file/<int:fileId>')
def download_orginal(fileId):


	if Document.query.filter_by(id=fileId).first() != None:
		
		file = creat_Docx_from_id(fileId)
	
		docx_id = Product.query.filter_by(document_id=fileId, type='docx').first().id
		update_or_create_Statistic(docx_id, 'download')
	
		strIO = BytesIO(file[0])
		strIO.seek(0)
		return send_file(strIO, as_attachment=True, attachment_filename=file[1].encode("ascii","ignore"), mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

	else:
		abort(404)