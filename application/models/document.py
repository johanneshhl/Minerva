 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from io import BytesIO
import datetime


from application.models.converts.DOCX_TO_HTML import DATA_HTML
from application.models.converts.HTML_TO_EPUB import HTML_TO_EPUB
import zipfile

from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash, jsonify
from application.controlers.document import *
from application.database.database import Document, User, Product, Statistic












def get_docx_info(file):

	'''

		Henter infomation fra docx fil
		retuner json med metadata

	'''

	filename = file.filename.split(".docx",1)[0] #find fil navn
	fileBlob = BytesIO(file.read()) #Læs docx i hukommelse

	newDocument = DATA_HTML(fileBlob, filename) # nyt objekt fra filblob og filnavn

	category = '' #ny variable 
	
	for i, item in enumerate(newDocument.documentCategory): #Loop over emner og lav komma string
		if i == (len(newDocument.documentCategory)-1):
			category += item
		else: 
			category += item + ','

	return jsonify(documnetName=str(newDocument.documentTitle), documentSubtitle=str(None), documentDescription=str(newDocument.documentDescription), documentSubject=str(newDocument.documentSubject), documentCategory=str(category), documentEducation_level='')
		



def Add_Docx_to_database(file, metadata):
	
	'''

		Henter infomation fra docx fil
		Og hvis der sendes metadata med, overskriver de docx standart metadater 

		Derefter oprettet dockument i databasen

	'''

	filename = file.filename.split(".docx",1)[0] #filnavn
	
	fileBlob = BytesIO(file.read()) #Læs docx i hukommelse

	newDocument = DATA_HTML(fileBlob, filename) # nyt objekt fra filblob og filnavn

	category = ''
	for i, item in enumerate(newDocument.documentCategory): #Loop over emner og lav komma string
		if i == (len(newDocument.documentCategory)-1):
			category += item
		else: 
			category += item + ','


	if 'documentTitle' in metadata:  # er 'documentTitle' i metadata så lav ny variable
		name = u''+str(metadata['documentTitle'])
	else:
		name = u''+str(newDocument.documentTitle)



	if 'documentSubtitle' in metadata: # er 'documentSubtitle' i metadata så lav ny variable
		subtitle = u''+str(metadata['documentSubtitle'])
	else:
		subtitle = u''+str(None)
	

	if 'documentDescription' in metadata: # er 'documentDescription' i metadata så lav ny variable
		description = u''+str(metadata['documentDescription'])
	else:
		description = u''+str(newDocument.documentDescription)
	


	if 'documentSubject' in metadata: # er 'documentSubject' i metadata så lav ny variable
		subject = u''+str(metadata['documentSubject'])
	else:
		subject = u''+str(newDocument.documentSubject)	



	if 'documentTopic' in metadata: # er 'documentTopic' i metadata så lav ny variable
		topic = u''+str(metadata['documentTopic'])
	else:
		topic = u''+str(category)	



	if 'documentEducation_level' in metadata: # er 'documentEducation_level' i metadata så lav ny variable
		education_level = u''+str(metadata['documentEducation_level'])
	else:
		education_level = u''



	#opret nyt dokument objekt med al metadaten
	addDocument = Document(g.userId, name, subtitle, description, subject, topic, education_level, fileBlob.getvalue())
	
	db.session.add(addDocument) #tilføj til databas 
	db.session.commit()	#affyr sql 

	#og send til dokument visnings siden
	return redirect(url_for('viewDocument', fileId=addDocument.id, _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))






def update_document_from_dict(fileId, metadataDict, file):

	'''

		Updater dokument fra metadata Dict og eller fil

	'''

	
	orgDocument = Document.query.filter_by(id=fileId).first() # hente dokument

	if int(orgDocument.user_id) == int(g.userId): #hvis brugeren er ejer af dokument

		orgDocument.version = int(orgDocument.version) + 1 #opdater version 1+1
		orgDocument.created = datetime.datetime.now() # ny dato
		
		if 'documentTitle' in metadataDict: # er 'documentTitle' i metadataDict så opdater dokument.'documentTitle'
			orgDocument.name = u''+str(metadataDict['documentTitle'])

		if 'documentSubtitle' in metadataDict: # er 'documentSubtitle' i metadataDict så opdater dokument.'documentSubtitle'
			orgDocument.subtitle = u''+str(metadataDict['documentSubtitle'])
		
		if 'documentDescription' in metadataDict: # er 'documentDescription' i metadataDict så opdater dokument.'documentDescription'
			orgDocument.description = u''+str(metadataDict['documentDescription'])

		if 'documentSubject' in metadataDict: # er 'documentSubject' i metadataDict så opdater dokument.'documentSubject'
			orgDocument.subject = u''+str(metadataDict['documentSubject'])

		if 'documentTopic' in metadataDict: # er 'documentTopic' i metadataDict så opdater dokument.'documentTopic'
			orgDocument.topic = u''+str(metadataDict['documentTopic'])
		
		if 'documentEducation_level' in metadataDict: # er 'documentEducation_level' i metadataDict så opdater dokument.'documentEducation_level'
			orgDocument.education_level = u''+str(metadataDict['documentEducation_level'])
		

		fileBlob = BytesIO(file.read()) #Læs fil i hukommelse 
		
		if (zipfile.is_zipfile(fileBlob)): #Er fil docx ? - tilføjet pga. fejl i firefox med drag and drop
			orgDocument.original_file = fileBlob.getvalue()

		db.session.commit() #affyr sql 

		return redirect(url_for('viewDocument', fileId=orgDocument.id, _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))

	else:
		abort(403) #ellers set "not allowed http error"






def create_epub_from_id(fileId):


	'''

		Opret epub fra fil id, og skrive en kopi til database som cache 
		Eller hvis filen "produketet" allerede findes som cache og er samme version som dokumentet, så hent den.


		retuner Epub blob og dokuments navn

	'''


	
	orgDocument = Document.query.filter_by(id=fileId).first() #Orginal dokumenet
	epub = Product.query.filter_by(document_id=orgDocument.id, type='epub').first() # Epub filen enten Object eller None


	if epub == None: #hvis epub er None 

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
		#hvis version på epub'en er mindre end orginal dokumenetet's
		#så opdater epub'en med data fra original dokumenet 

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

		#Hvis version på epub'en er den samme som orginal dokumenetet's
		#så brug epub'ens blob

		elif epub.version == orgDocument.version:

			return [epub.file_blob, orgDocument.name]






def create_HTML_from_id(fileId):
	
	'''

		Opret HTML fra fil id, og skrive en kopi til database som cache 
		Eller hvis filen "produketet" allerede findes som cache og er samme version som dokumentet, så hent den.


		retuner HTML blob og dokuments navn

	'''

	orgDocument = Document.query.filter_by(id=fileId).first() #Orginal dokumenet
	HTML = Product.query.filter_by(document_id=orgDocument.id, type='html').first() # HTML filen enten Object eller None

	if HTML == None: #hvis HTML er None 

		author = User.query.filter_by(id=orgDocument.user_id).first()
		authorName = author.firstname + ' ' + author.lastname

		fileBlob = BytesIO(orgDocument.original_file)
		Data = DATA_HTML(fileBlob, '')

		HTML_text = Data.documentContent
	
		addHTML = Product(orgDocument.id, 'html', HTML_text.encode())
		addHTML.version = int(orgDocument.version)

		db.session.add(addHTML)
		db.session.commit()

		return [HTML_text, orgDocument.name]

	else:
		#hvis version på HTML'en er mindre end orginal dokumenetet's
		#så opdater HTML'en med data fra original dokumenet 

		if HTML.version < orgDocument.version:

			author = User.query.filter_by(id=orgDocument.user_id).first()
			authorName = author.firstname + ' ' + author.lastname
			
			fileBlob = BytesIO(orgDocument.original_file)
			Data = DATA_HTML(fileBlob, '')

			HTML_text = Data.documentContent

			HTML.version = int(orgDocument.version)
			HTML.file_blob = HTML_text.encode()
			HTML.created = datetime.datetime.now()

			db.session.commit()

			return [HTML_text, orgDocument.name]

		#Hvis version på HTML'en er den samme som orginal dokumenetet's
		#så brug HTML'ens blob

		elif HTML.version == orgDocument.version:

			return [HTML.file_blob, orgDocument.name]







def creat_Docx_from_id(fileId):

	'''

		Opret DOCX fra fil id, og skrive en kopi til database som cache 
		Eller hvis filen "produketet" allerede findes som cache og er samme version som dokumentet, så hent den.


		retuner DOCX blob og dokuments navn

	'''

	
	orgDocument = Document.query.filter_by(id=fileId).first()  #Orginal dokumenet
	docx = Product.query.filter_by(document_id=orgDocument.id, type='docx').first() # DOCX filen enten Object eller None



	if docx == None: #hvis epub er None 
		

		
		fileBlob = orgDocument.original_file

		addDocx = Product(orgDocument.id, 'docx', fileBlob)

		db.session.add(addDocx)
		db.session.commit()
	

		return [fileBlob, orgDocument.name]


	#hvis version på DOCX'en er mindre end orginal dokumenetet's
	#så opdater DOCX'en med data fra original dokumenet 

	elif docx.version < orgDocument:

		fileBlob = orgDocument.original_file
		
		docx.version = int(orgDocument.version)
		docx.file_blob = fileBlob
		docx.created = datetime.datetime.now()

		db.session.commit()

		return [fileBlob, orgDocument.name]

	#Hvis version på DOCX'en er den samme som orginal dokumenetet's
	#så brug DOCX'ens blob

	elif docx.version == orgDocument.version:

		return [docx.file_blob, orgDocument.name]











def update_or_create_Statistic(productId, download_or_display):

	''' 
		Opdater eller lav ny stastik

	'''


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









