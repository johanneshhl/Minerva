 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from application import db, bcrypt
import datetime





class User(db.Model):
	'''
		
		Bruger Database model,
		fx:
			id = 1
			firstname = Johannes
			lastname = Hvilsom
			email = Johannes@hvilsom.dk
			password = $2a$07$ywncG5/nYOFO4tiBPH9sz.m5dMn8nceXVcvxirQm97BPxNHSKqOpy :: som er bcrypt med 7 runs af "1234567890" 
			created = 2015-06-07 15:07:20
			last_login = 2015-06-07 15:07:20

		Og en relationship key ( en til mange )
			Bruger ➔ Document



		Tager 4 inputs
		Fornavn, efternavn, email & rå emial (før bcrypt)


	'''

	id = db.Column(db.Integer, primary_key=True)
	
	firstname = db.Column(db.String(64), nullable=False)
	lastname = db.Column(db.String(64), nullable=False)

	email = db.Column(db.String(128), nullable=False, unique=True)

	password = db.Column(db.String(120), nullable=False)

	created = db.Column(db.DateTime)
	last_login = db.Column(db.DateTime)

	user_documents = db.relationship('Document', backref='user', lazy='dynamic')


	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = bcrypt.generate_password_hash(password, 7) #hasher kodeordet med bcrypt med 7 kørsler, det optimale ville være 12 men pga. min nuværedene servers hastighed sat til 7 
		self.created = datetime.datetime.now()
		self.last_login = self.created

	def __repr__(self):
		return '<User %r>' % self.id







class Document(db.Model):

	'''
	
		Document Database model,
		fx:
			id = 1
			user_id = 1
			version = 5
			created = 2015-06-09 11:26:35
			name = Dokument titel
			subtitle = Dokument undertitel
			description = Dokument beskrivelse
			subject = Dokumentes fag
			topic = Dokument emne
			education_level = skole nivue ( Folkeskole, Ungdomsuddannelse og Videregående uddannelser)
			original_file = orginal fil blob (brugers pga. applicationen køres på virtuel server)

	
		Og en relationship key ( en til mange )
			Document ➔ produkter
	
	
	
		Tager 8 inputs
		Bruger id, Navn, undertitel, beskrivelse, fag, emne, skole nivue, orginal fil blob


	'''


	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	version = db.Column(db.Integer, default=1)
	created = db.Column(db.DateTime)

	name = db.Column(db.String(64), nullable=False)
	subtitle = db.Column(db.String(64))

	description = db.Column(db.String(2048), nullable=False)

	subject = db.Column(db.String(64), nullable=False, default='Dansk')
	topic = db.Column(db.String(128))

	education_level = db.Column(db.String(128))

	original_file = db.Column(db.LargeBinary, nullable=False)

	document_products = db.relationship('Product', backref='document', lazy='dynamic')


	def __init__(self, user_id, name, subtitle, description, subject, topic, education_level, original_file):
		
		self.user_id = user_id

		self.name = name
		self.subtitle = subtitle

		self.description = description
		self.subject = subject
		self.topic = topic
		self.education_level = education_level

		self.original_file = original_file

		self.created = datetime.datetime.now()


	def __repr__(self):
		return self.id






class Product(db.Model):


	'''
	
		Product Database model,
		fx:
			id = 1
			document_id = 1
			type = produkt type ( Epub, HTML & Docx ) + på sigt pdf
			version = 5
			created = 2015-06-09 11:26:35
			file_blob = fil blob (brugers pga. applicationen køres på virtuel server)

	
		Og en relationship key ( en til en )
			Product ➔ statisk
	
	
	
		Tager 3 inputs
		Document id, type & fil blob


	'''



	id = db.Column(db.Integer, primary_key=True)
	document_id = db.Column(db.Integer, db.ForeignKey('document.id'))

	type = db.Column(db.String(64), nullable=False)

	version = db.Column(db.Integer, default=1)

	created = db.Column(db.DateTime)

	file_blob = db.Column(db.LargeBinary, nullable=False)

	document_statistic = db.relationship('Statistic', backref='product', lazy='dynamic')


	def __init__(self, document_id, type, file_blob):
		self.document_id = document_id
		self.type = type
		self.file_blob = file_blob
		self.created = datetime.datetime.now()

	def __repr__(self):
		return '<Product %r>' % self.id





class Statistic(db.Model):

	'''
	
		Statisk Database model,
		fx:
			id = 1
			produkt id = 1
			displays = 39
			downloads = 1020

	
		Tager 3 inputs
		produkt id, displays & downloads


	'''

	id = db.Column(db.Integer, primary_key=True)
	document_id = db.Column(db.Integer, db.ForeignKey('product.id'))

	displays = db.Column(db.Integer)
	downloads = db.Column(db.Integer)

	def __init__(self, document_id, displays, downloads):
		self.document_id = document_id
		self.displays = displays
		self.downloads = downloads

	def __repr__(self):
		return '<Statistic %r>' % self.id




