#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
		Title:	Open Office XML Converter
	
  Description:	Convert OOXML to Minerva-HTML
	
		Input:	Docx/Zip
	   Output:	Minerva-HTML

		 Date:	18. Maj 2015

'''
import zipfile
import base64
from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash
import cgi

from bs4 import BeautifulSoup
from colour import Color




class DATA_HTML():
	

	def __init__(self, docx, filename):

		self.fileName = filename
		self.isZip = zipfile.is_zipfile(docx)
		if self.isZip:
			
			self.Zip = zipfile.ZipFile(docx)
			self.XML = BeautifulSoup(self.Zip.read('word/document.xml'),from_encoding="utf-8")
			
			self.MetaXML = BeautifulSoup(self.Zip.read('docProps/core.xml'),from_encoding="utf-8")
			if 'word/numbering.xml' in self.Zip.namelist():
				self.Numbering = BeautifulSoup(self.Zip.read('word/numbering.xml'),from_encoding="utf-8")
			
			self.RelationshipsXML = BeautifulSoup(self.Zip.read('word/_rels/document.xml.rels'),from_encoding="utf-8")
				
			self.documentReady = True

			self.documentTitle = self.getTitle()
			self.documentCreator = self.getCreator()
			self.documentSubject = self.getSubject()
			self.documentDescription = self.getDescription()
			self.documentCategory = self.getCategory()
			self.documentContent = self.getContent()

		else:

			self.documentReady = False

			self.documentTitle = 'Not a zipfile'
			self.documentCreator = 'Not a zipfile'
			self.documentDescription = 'Not a zipfile'
			self.documentSubject = 'Not a zipfile'

	def getTitle(self):

		'''
			Hent Dokument titel,
			prøver Metadata'en først,
			der efter Dokumentet,

			og fil navn som fallback

		'''

		documentTitle = u''

		if self.MetaXML.find('dc:title') != None:
			documentTitle = self.MetaXML.find('dc:title').string

			if documentTitle == None or documentTitle == '':
				documentTitle = self.fileName

		else:
			documentTitle = self.fileName	


		return documentTitle


	def getCreator(self):

		'''

			Hent Dokuments forfatter
			Prøver Metadata filen, 
			ellers retuner None

		'''
	
		documentCreator = u''
		if self.MetaXML.find('dc:creator') != None:
			documentCreator = self.MetaXML.find('dc:creator').string
		else: 
			documentCreator = None

		return documentCreator




	def getDescription(self):
		'''

			Hent Dokuments beskrivelse
			Prøver Metadata filen, 
			ellers retuner None

		'''
		documentDescription = u''

		if self.MetaXML.find('dc:description') != None:
			documentDescription = self.MetaXML.find('dc:description').string
		else:
			documentDescription = None



	def getSubject(self):

		'''
			
			Hent Dokuments kategori
			Prøver Metadata filen, 
			ellers retuner None

		'''

		documentSubject = u''

		if self.MetaXML.find('dc:subject') != None:
			documentSubject = self.MetaXML.find('dc:subject').string
		else:
			documentSubject = None

		return documentSubject


	def getCategory(self):

		'''
			
			Hent Dokuments kategori
			Prøver Metadata filen, 
			ellers retuner None

		'''


		if self.MetaXML.find('cp:category') != None:
			documentCategory = self.MetaXML.find('cp:category').string
		else:
			documentCategory = None
			
		return documentCategory







	def getContent(self):

		'''
			Hent Dokuments indhold og retuner Minerva-HTML
			Prøver Metadata filen, 
			ellers retuner None

		'''

		documentContent = u''

		for node in self.XML.find('w:body').children:

			#find den Node i en liste 
			#if node.find('w:numpr') != None:
			#	documentContent += self.listConversion(node)
			if node.find('w:numpr') != None:
				if node.previous_sibling == None or int(node.find('w:ilvl')['w:val']) == 0:
					documentContent += self.listConversion(node)
			elif node.find('w:drawing') != None:
				documentContent += self.imageConversion(node)
			elif node.name == 'w:p' and node.find('w:numpr') == None:
				documentContent += self.paragraphConversion(node)
			elif node.name == 'w:tbl':
				documentContent += self.tableConversoin(node)
				
		return documentContent





	def paragraphConversion(self, paragraph):
		
		'''
			Konvater paragraph 
			fra OOXML til Minerva-HTML
		'''



		paragraphNode = u''

		blockNodeDict = dict(
			Overskrift1='h1',
			Overskrift2='h2',
			Overskrift3='h3',
			Overskrift4='h4',
			Overskrift5='h5',
			Overskrift6='h6',
			Heading1='h1',
			Heading2='h2',
			Heading3='h3',
			Heading4='h4',
			Headng5='h5',
			Heading6='h6'
		)

		if (paragraph.find('w:pstyle') != None) and (paragraph.find('w:pstyle')['w:val'] in blockNodeDict):
			nodeName = blockNodeDict[paragraph.find('w:pstyle')['w:val']]
		
		else:
			nodeName = 'p'



		paragraphNode = "<{0}>{1}</{0}>".format(nodeName, self.runConversion(paragraph))

		if len(self.runConversion(paragraph)) > 1:
			return paragraphNode
		else: 
			return ''







	def runConversion(self, paragraph):

		'''
			Konvater "runs" i en OOXML paragraph

		'''
		inlineBlockNodeArray = dict(
							i='i',
							b='b',
							u='u',
							strike='del',
						)


		runs = u''
		for run in paragraph.findAll('w:r'):
			openingNode = u''
			closeingNode = u''
			textNode = u'' + self.textConversion(run)
			
			if run.parent.name == 'w:hyperlink':
				if ('w:anchor' in (run.parent.attrs)) == False:
					openingNode = '<{0}>{1}'.format(self.createHyperlink(run)[0], openingNode)
					closeingNode = "{1}</{0}>".format(self.createHyperlink(run)[1], closeingNode)


			if run.find('w:rpr') != None:
				for inlineBlock in run.find('w:rpr').children:
					
					if inlineBlock.name.split(":",1)[1] in inlineBlockNodeArray:
						nodeName = inlineBlock.name.split(":",1)[1]

						openingNode = "<{0}>{1}".format(nodeName, openingNode)
						closeingNode = "{1}</{0}>".format(nodeName, closeingNode)

					elif inlineBlock.name == 'w:highlight':
						nodeName = '<ins>'
						closeingNode = '<ins>'


					elif inlineBlock.name == 'w:color':
						if inlineBlock['w:val'] != 'auto':
							nodeName = 'span'
							colorName = "%s" % Color(u'#'+inlineBlock['w:val'])
							
							openingNode = '<{0} style="color:{2}">{1}'.format(nodeName, openingNode, colorName)
							closeingNode = "{1}</{0}>".format(nodeName, closeingNode)
							
							

			runs += "{0}{1}{2}".format(openingNode, textNode, closeingNode)

		return runs




	def createHyperlink(self, run):

		'''
			Lav hyperlink fra run

		'''

		nodeName = 'a'
		rID = run.parent['r:id']
		hyperlink = self.RelationshipsXML.find(id=rID)

		return ['a href="{0}"'.format(hyperlink['target']).replace('&','&amp;'),'a']




	def textConversion(self, run):

		'''
			lav tekst fra run 

		'''

		text = u''
		for textNode in run.children:
			if textNode.name == 'w:br':
				text += '<br />'
			elif textNode.name =='w:tab':
				text += '&nbsp;&nbsp;&nbsp;&nbsp;'
			elif textNode.name == 'w:t':
				text += cgi.escape(textNode.string)
			else:
				text = text
		return text




	def imageConversion(self, node):


		'''
			Lav IMG med base64 string 

		'''

		imageNode = u''

		imageID = node.find('w:drawing').find('a:blip')['r:embed']
		imageName = 'word/' + self.RelationshipsXML.find('relationship', attrs={"id": imageID})['target']
		imageExt = imageName.split(".",1)[1]

		imageBase64 = self.Zip.read(imageName).encode("base64")


		imageNode = '<img src="data:image/{};base64,{}" alt="Billede" />'.format(imageExt, imageBase64)

		return imageNode





	def listConversion(self, node):

		'''
			Konvater liste 
			fra OOXML til Minerva-HTML

			Bullets og Numringer virker

			kan ikke hoppe et niveu over :) 
		'''



		selfNode = ''
		selfType = self.getListType(node.find('w:numid')['w:val'])
		
		level = int(node.find('w:ilvl')['w:val'])

		realChildren = []
		realSibling = []
		
		if (node.previous_sibling == None) or (node.previous_sibling.find('w:numid') == None) or (self.getListType(node.previous_sibling.find('w:numid')['w:val']) != selfType):
			selfNode += '<{}>'.format(selfType)

		if level == 0:
			selfNode += '<li>'+ self.runConversion(node)
		else:
			selfNode += self.runConversion(node)

		for sibling in node.next_siblings:
			if (sibling.find('w:numpr') == None):
				break
			elif int(sibling.find('w:ilvl')['w:val']) < (int(level)+1):
				break
			elif self.getListType(sibling.find('w:numid')['w:val']) != selfType:
				break
			elif int(sibling.find('w:ilvl')['w:val']) == (int(level)+1):
				realChildren.append(sibling)
		
		if realChildren != []:
			selfNode += '<ul>'
			
			for child in realChildren:
				selfNode += '<li>{}</li>'.format(self.listConversion(child))

		if realChildren != []:
			selfNode += '</ul>'

		if level == 0:
			selfNode += '</li>'
		else:
			pass

				
		if (node.next_sibling == None) or (node.next_sibling.find('w:numid') == None) or (self.getListType(node.next_sibling.find('w:numid')['w:val']) != selfType):
			selfNode += '</{}>'.format(selfType)




		listNode = selfNode
		return listNode





	def getListType(self, listType):

		listTypes = dict(bullet='ul', decimal='ol')

		listTypeNode = self.Numbering.find('w:num',attrs={"w:numid": listType})
		listTypeNr = listTypeNode.find('w:abstractnumid')['w:val']
		
		listTypeString = self.Numbering.find('w:abstractnum', attrs={"w:abstractnumid": listTypeNr}).find('w:numfmt')['w:val']
		
		return listTypes[listTypeString]







	def tableConversoin(self, table):
		tableNode = u''
		tableNode = "<{0}><{1}>{2}</{1}></{0}>".format('table class="table-bordered"','tbody', self.rowConversion(table))

		return tableNode





	def rowConversion(self, table):

		'''
			Konvater rækker "w:td"
			fra OOXML til Minerva-HTML
		'''

		rowNodes = u''

		for row in table.children:
			if row.name == 'w:tr':
				rowNodes += "<{0}>{1}</{0}>".format('tr', self.columConversion(row))

		return rowNodes




	def columConversion(self, row):

		'''
			Konvater koloner "w:tc"
			fra OOXML til Minerva-HTML
		'''
		

		columNodes = u''
		
		for colum in row.children:
			if colum.name == 'w:tc':
				
				content = u''

				for paragraph in colum.children:
					if paragraph.name == 'w:p':
						content += self.runConversion(paragraph)
				
				columNodes += "<{0}>{1}</{0}>".format('td', content)
				
		return columNodes




