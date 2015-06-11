 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from io import BytesIO
import datetime


from application.models.converts.DOCX_TO_HTML import DATA_HTML
from application.models.converts.HTML_TO_EPUB import HTML_TO_EPUB

from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash, jsonify
from application.controlers.document import *
from application.database.database import Document, User, Product, Statistic












def get_docx_info(file):
	filename = file.filename.split(".docx",1)[0]
	fileBlob = BytesIO(file.read())
	#fileBlob.content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
	newDocument = DATA_HTML(fileBlob, filename)

	category = ''
	
	for i, item in enumerate(newDocument.documentCategory):
		if i == (len(newDocument.documentCategory)-1):
			category += item
		else: 
			category += item + ','

	return jsonify(documnetName=str(newDocument.documentTitle), documentSubtitle=str(None), documentDescription=str(newDocument.documentDescription), documentSubject=str(newDocument.documentSubject), documentCategory=str(category), documentEducation_level='')
		



def Add_Docx_to_database(file, metadata):
	
	filename = file.filename.split(".docx",1)[0]
	
	fileBlob = BytesIO(file.read())

	newDocument = DATA_HTML(fileBlob, filename)

	category = ''
	for i, item in enumerate(newDocument.documentCategory):
		if i == (len(newDocument.documentCategory)-1):
			category += item
		else: 
			category += item + ','


	app.logger.info(metadata)


	if 'documentTitle' in metadata:
		name = u''+str(metadata['documentTitle'])
	else:
		name = u''+str(newDocument.documentTitle)



	if 'documentSubtitle' in metadata:
		subtitle = u''+str(metadata['documentSubtitle'])
	else:
		subtitle = u''+str(None)
	

	if 'documentDescription' in metadata:
		description = u''+str(metadata['documentDescription'])
	else:
		description = u''+str(newDocument.documentDescription)
	


	if 'documentSubject' in metadata:
		subject = u''+str(metadata['documentSubject'])
	else:
		subject = u''+str(newDocument.documentSubject)	



	if 'documentTopic' in metadata:
		topic = u''+str(metadata['documentTopic'])
	else:
		topic = u''+str(category)	



	if 'documentEducation_level' in metadata:
		education_level = u''+str(metadata['documentEducation_level'])
	else:
		education_level = u''




	addDocument = Document(g.userId, name, subtitle, description, subject, topic, education_level, fileBlob.getvalue())
	db.session.add(addDocument)
	db.session.commit()

	return redirect(url_for('viewDocument', fileId=addDocument.id ))






def update_document_from_dict(fileId, metadataDict, file):
	
	orgDocument = Document.query.filter_by(id=fileId).first()

	if int(orgDocument.user_id) == int(g.userId):

		orgDocument.version = int(orgDocument.version) + 1
		orgDocument.created = datetime.datetime.now()
		
		if 'documentTitle' in metadataDict:
			orgDocument.name = u''+str(metadataDict['documentTitle'])

		if 'documentSubtitle' in metadataDict:
			orgDocument.subtitle = u''+str(metadataDict['documentSubtitle'])
		
		if 'documentDescription' in metadataDict:
			orgDocument.description = u''+str(metadataDict['documentDescription'])

		if 'documentSubject' in metadataDict:
			orgDocument.subject = u''+str(metadataDict['documentSubject'])

		if 'documentTopic' in metadataDict:
			orgDocument.topic = u''+str(metadataDict['documentTopic'])
		
		if 'documentEducation_level' in metadataDict:
			orgDocument.education_level = u''+str(metadataDict['documentEducation_level'])
		
		#app.logger.info(file)
		if file != None:
			fileBlob = BytesIO(file.read())
			orgDocument.original_file = fileBlob.getvalue()

		db.session.commit()

		return redirect(url_for('viewDocument', fileId=orgDocument.id))

	else:
		abort(403)






def create_epub_from_id(fileId):
	
	orgDocument = Document.query.filter_by(id=fileId).first()
	epub = Product.query.filter_by(document_id=orgDocument.id, type='epub').first()


	if epub == None:
		author = User.query.filter_by(id=orgDocument.user_id).first()
		authorName = author.firstname + ' ' + author.lastname
		
		fileBlob = BytesIO(orgDocument.original_file)
		Data = DATA_HTML(fileBlob, '')

		meta = dict(title=orgDocument.name, subject=orgDocument.subject, category=orgDocument.topic, description=orgDocument.description, lang='da', creator=authorName)

		newEpub = HTML_TO_EPUB(Data.documentContent, meta)

		addEpub = Product(orgDocument.id, 'epub', newEpub.createEpub())
		
		db.session.add(addEpub)
		db.session.commit()

		return [newEpub.createEpub(), orgDocument.name]

	else:
		if epub.version < orgDocument.version:
			author = User.query.filter_by(id=orgDocument.user_id).first()
			authorName = author.firstname + ' ' + author.lastname
			
			fileBlob = BytesIO(orgDocument.original_file)
			Data = DATA_HTML(fileBlob, '')

			meta = dict(title=orgDocument.name, subject=orgDocument.subject, category=orgDocument.topic, description=orgDocument.description, lang='da', creator=authorName)
			newEpub = HTML_TO_EPUB(Data.documentContent, meta)


			epub.version = int(orgDocument.version)
			epub.file_blob = newEpub.createEpub()
			epub.created = datetime.datetime.now()

			db.session.commit()

			return [newEpub.createEpub(), orgDocument.name]

		elif epub.version == orgDocument.version:

			return [epub.file_blob, orgDocument.name]






def create_HTML_from_id(fileId):
	
	orgDocument = Document.query.filter_by(id=fileId).first()
	HTML = Product.query.filter_by(document_id=orgDocument.id, type='html').first()

	if HTML == None:
		author = User.query.filter_by(id=orgDocument.user_id).first()
		authorName = author.firstname + ' ' + author.lastname

		fileBlob = BytesIO(orgDocument.original_file)
		Data = DATA_HTML(fileBlob, '')

		HTML_text = Data.documentContent
		
		addHTML = Product(orgDocument.id, 'html', HTML_text)
		addHTML.version = int(orgDocument.version)

		db.session.add(addHTML)
		db.session.commit()

		return [HTML_text, orgDocument.name]

	else:
		if HTML.version < orgDocument.version:

			author = User.query.filter_by(id=orgDocument.user_id).first()
			authorName = author.firstname + ' ' + author.lastname
			
			fileBlob = BytesIO(orgDocument.original_file)
			Data = DATA_HTML(fileBlob, '')

			HTML_text = Data.documentContent

			HTML.version = int(orgDocument.version)
			HTML.file_blob = HTML_text
			HTML.created = datetime.datetime.now()

			db.session.commit()

			return [HTML_text, orgDocument.name]


		elif HTML.version == orgDocument.version:

			return [HTML.file_blob, orgDocument.name]







def creat_Docx_from_id(fileId):
	
	orgDocument = Document.query.filter_by(id=fileId).first()
	docx = Product.query.filter_by(document_id=orgDocument.id, type='docx').first()



	if docx == None:
		
		fileBlob = orgDocument.original_file

		addDocx = Product(orgDocument.id, 'docx', fileBlob)

		db.session.add(addDocx)
		db.session.commit()
	

		return [fileBlob, orgDocument.name]


	elif docx.version < orgDocument:

		fileBlob = orgDocument.original_file
		
		docx.version = int(orgDocument.version)
		docx.file_blob = fileBlob
		docx.created = datetime.datetime.now()

		db.session.commit()

		return [fileBlob, orgDocument.name]


	elif docx.version == orgDocument.version:

		return [docx.file_blob, orgDocument.name]











def update_or_create_Statistic(productId, download_or_display):

	statisticNode = Statistic.query.filter_by(document_id=productId).first()


	if statisticNode == None:

		newStatistic = Statistic(productId, 1, 1)

		db.session.add(newStatistic)
		db.session.commit()

	else:
		if download_or_display == 'download':
			statisticNode.downloads = (int(statisticNode.downloads)+1)
		else:
			statisticNode.displays = (int(statisticNode.displays)+1)			

		db.session.commit()

	return True










