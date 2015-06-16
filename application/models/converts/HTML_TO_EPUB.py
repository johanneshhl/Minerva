#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
		Title:	EPUB Createtor
	
  Description:	Convert HTML to EPUB
	
		Input:	Data-HTML
	   Output:	EPUB

		 Date:	29. Maj 2015

'''
from application import app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash, jsonify
import zipfile
import StringIO
import uuid
import time
import cgi
#from PIL import Image
#from PIL import ImageFont, ImageDraw
import base64
from bs4 import BeautifulSoup




class HTML_TO_EPUB(object):

	def __init__(self, DATA_HTML, METADATA):

		'''
			Lav Epub fra data-html

		'''

		self.DATA_HTML = BeautifulSoup(DATA_HTML, from_encoding="utf-8")
		self.UUDI = '{0}{1}'.format('urn:uuid:',str(uuid.uuid4()))

		if METADATA['title'] != None:
			self.documentTitle = cgi.escape(METADATA['title'])
		else:
			self.documentTitle = 'None'
		self.documentCreator = cgi.escape(METADATA['creator'])
		self.documentDescription = cgi.escape(METADATA['description'])
		self.documentSubject = cgi.escape(METADATA['subject'])
		self.documentCategory = cgi.escape(METADATA['category'])
	
		self.documentLang = METADATA['lang']

	def getChapters(self):

		'''	
			Hent kapitler 
			fra DATA_HTML

		'''


		html = []
		if self.DATA_HTML.find_all("h1") == []:
			node = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title>{0}</title><link rel="stylesheet" type="text/css" href="css/style.css"></link></head><body>{1}</body></html>'.format('No title',unicode(self.DATA_HTML))
			html = [['chapter001','No title', node]]
		else:
			x = 0
			for h1 in self.DATA_HTML.find_all("h1"):
				x = x+1
				chapterTitle = h1.text
				chapterString = u'chapter%03d' % (x)

				node = u''+unicode(h1)
				
				for tag in h1.next_siblings:

					if tag.name == "h1":
						break
					else:
						node += unicode(tag)



				node = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title>{0}</title><link rel="stylesheet" type="text/css" href="css/style.css"></link></head><body>{1}</body></html>'.format(chapterTitle,node)


				html.append([chapterString, chapterTitle, node])

		return html



	def createOpf(self):

		'''
			lav content.opf 
			Epub metadata fil


		'''

		title = "<dc:title>{}</dc:title>".format(self.documentTitle)


		app.logger.info(self.documentCreator)
		firstName = self.documentCreator.split(" ",1)[0]
		lastName = self.documentCreator.split(" ",1)[1]

		creator = "<dc:creator opf:file-as='{1}, {0}' opf:role='aut'>{0} {1}</dc:creator>".format(firstName, lastName)

		date = "<dc:date>{0}</dc:date>".format(time.strftime("%Y"))

		identifier = "<dc:identifier id='bookid'>{0}</dc:identifier>".format(self.UUDI)

		language = "<dc:language>{}</dc:language>".format(self.documentLang)

		description = "<dc:description>{}</dc:description>".format(self.documentDescription)

		subject = "<dc:subject>{}</dc:subject>".format(self.documentSubject)

		#cover = '<meta content="cover-image" name="cover"/>'
		metadata = '<metadata>'+ title + creator + date +identifier + language + description + subject + '</metadata>'

		manifestItems = '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>'
		manifestItems += '<item href="css/style.css" id="css" media-type="text/css"/>'
		#manifestItems += '<item href="images/cover.jpg" id="cover-image" media-type="image/jpeg"/>'

		spineItems = u''

		chapters = self.getChapters()
		for chapter in chapters:
			manifestItems += '<item href="{0}.html" id="{0}" media-type="application/xhtml+xml"/>'.format(chapter[0])
			spineItems += '<itemref idref="{0}"/>'.format(chapter[0])


		manifest = '<manifest>'+ manifestItems + '</manifest>'
		spine = '<spine toc="ncx">' + spineItems + '</spine>'
		guide = '<guide><reference href="{0}.html" title="{1}" type="text"/></guide>'.format(chapters[0][0], chapters[0][1])


		package = '<package unique-identifier="bookid" version="2.0" xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">'
		package += metadata + manifest + spine + guide
		package += '</package>'


		return package


	def createTOC(self):

		'''
			Lav toc.ncx 


		'''


		head = u'<head>'
		head += '<meta content="{}" name="dtb:uid"/>'.format(self.UUDI)
		head += '<meta content="" name="dtb:depth"/><meta content="" name="dtb:totalPageCount"/><meta content="" name="dtb:maxPageNumber"/>'
		head += '</head>'

		title = '<docTitle><text>{}</text></docTitle>'.format(self.documentTitle)

		navMap = '<navMap>'

		chapters = self.getChapters()
		for i, chapter in enumerate(chapters):
			navMap += '<navPoint id="navpoint-{0}" playOrder="{1}"><navLabel><text>{2}</text></navLabel><content src="{3}.html"/></navPoint>'.format('%03d' % (i), i, chapter[1], chapter[0])
			
		navMap += '</navMap>'

		toc = '<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">'+ head + title + navMap + '</ncx>'

		return toc


	def createEpub(self):

		'''
			Lav epub i hukommelse

		'''


		chapters = self.getChapters()
		zipInMemmoryArcive = StringIO.StringIO()
		with zipfile.ZipFile(zipInMemmoryArcive, "w") as  myzip:
				
	
			#create Mimetype
			mimetype = 'application/epub+zip'
			myzip.writestr('mimetype',mimetype)

			#create Meta-inf
			conatiner = '<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
			myzip.writestr('META-INF/container.xml',conatiner)

			opf = self.createOpf()	
			myzip.writestr('OEBPS/content.opf', opf.encode('utf-8'))

			css = self.createStyle()
			myzip.writestr('OEBPS/css/style.css',css.encode('utf-8'))

			toc = self.createTOC()
			myzip.writestr('OEBPS/toc.ncx', toc.encode('utf-8'))

			#coverImage = self.createCover()
			#myzip.writestr('OEBPS/images/cover.jpg', coverImage)

			for chapter in chapters:
				myzip.writestr('OEBPS/'+chapter[0]+'.html', chapter[2].encode('utf-8'))

			print(myzip.namelist())
		

		return zipInMemmoryArcive.getvalue()





	def createStyle(self):

		'''
			Et hurtigt fix til at lave en css fil i epub'en 
			Baseret på typeplate 

		'''

		cssFileBase64 = '''
			@charset "UTF-8";
			/*!
			Typeplate : Starter Kit
			URL ........... http://typeplate.com
			Version ....... 2.1.0
			Github ........ https://github.com/typeplate/starter-kit
			Authors ....... Dennis Gaebel (@gryghostvisuals) & Zachary Kain (@zakkain)
			License ....... Creative Commmons Attribution 3.0
			License URL ... https://github.com/typeplate/starter-kit/blob/master/license.txt
			*/
			@font-face {
			  font-family: "Ampersand";
			  src: local("Georgia"), local("Garamond"), local("Palatino"), local("Book Antiqua");
			  unicode-range: U+0026; }
			@font-face {
			  font-family: "Ampersand";
			  src: local("Georgia");
			  unicode-range: U+270C; }
			.typl8-tera, .typl8-giga, .typl8-mega, .typl8-alpha, .typl8-beta, .typl8-gamma, h1, .typl8-delta, h2, .typl8-epsilon, h3, .typl8-zeta, h4, h5, h6 {
			  text-rendering: optimizeLegibility;
			  line-height: 1;
			  margin-top: 0;
			  color: #222; }
			
			blockquote + figcaption cite {
			  display: block;
			  font-size: inherit;
			  text-align: right; }
			
			body {
			  word-wrap: break-word; }
			
			pre code {
			  word-wrap: normal; }
			
			html {
			  font: normal 100%/1.65 serif; }
			
			body {
			  -webkit-hyphens: auto;
			  -moz-hyphens: auto;
			  -ms-hyphens: auto;
			  hyphens: auto;
			  color: #444; }
			
			.typl8-tera {
			  font-size: 117px;
			  font-size: 11.7rem;
			  margin-bottom: 70.90909px;
			  margin-bottom: 7.09091rem; }
			
			.typl8-giga {
			  font-size: 90px;
			  font-size: 9rem;
			  margin-bottom: 54.54545px;
			  margin-bottom: 5.45455rem; }
			
			.typl8-mega {
			  font-size: 72px;
			  font-size: 7.2rem;
			  margin-bottom: 43.63636px;
			  margin-bottom: 4.36364rem; }
			
			.typl8-alpha {
			  font-size: 60px;
			  font-size: 6rem;
			  margin-bottom: 36.36364px;
			  margin-bottom: 3.63636rem; }
			
			.typl8-beta {
			  font-size: 48px;
			  font-size: 4.8rem;
			  margin-bottom: 29.09091px;
			  margin-bottom: 2.90909rem; }
			
			.typl8-gamma, h1 {
			  font-size: 20px;
			  font-size: 2rem;
			  margin-bottom: 12.12121px;
			  margin-bottom: 1.21212rem; }
			
			.typl8-delta, h2 {
			  font-size: 13.333px;
			  font-size: 1.3333rem;
			  margin-bottom: 8.08061px;
			  margin-bottom: 0.80806rem; }
			
			.typl8-epsilon, h3 {
			  font-size: 11.6667px;
			  font-size: 1.16667rem;
			  margin-bottom: 7.07073px;
			  margin-bottom: 0.70707rem; }
			
			.typl8-zeta, h4, h5, h6 {
			  font-size: 10px;
			  font-size: 1rem;
			  margin-bottom: 6.06061px;
			  margin-bottom: 0.60606rem; }
			
			p {
			  margin: auto auto 1.5em; }
			  p + p {
			    text-indent: 1.5em;
			    margin-top: -1.5em; }
			
			small {
			  font-size: 65%; }
			
			input,
			abbr,
			acronym,
			blockquote,
			code,
			kbd,
			q,
			samp,
			var {
			  -webkit-hyphens: none;
			  -moz-hyphens: none;
			  -ms-hyphens: none;
			  hyphens: none; }
			
			pre {
			  white-space: pre; }
			  pre code {
			    white-space: -moz-pre-wrap;
			    white-space: pre-wrap; }
			
			code {
			  white-space: pre;
			  font-family: monospace; }
			
			abbr {
			  -webkit-font-variant: small-caps;
			  -moz-font-variant: small-caps;
			  -ms-font-variant: small-caps;
			  font-variant: small-caps;
			  font-weight: 600;
			  text-transform: lowercase;
			  color: gray; }
			  abbr[title]:hover {
			    cursor: help; }
			
			.typl8-drop-cap:first-letter {
			  float: left;
			  margin: 10px 10px 0 0;
			  padding: 0 20px;
			  font-size: 4em;
			  font-family: inherit;
			  line-height: 1;
			  text-indent: 0;
			  background: transparent;
			  color: inherit; }
			
			p + .typl8-drop-cap {
			  text-indent: 0;
			  margin-top: 0; }
			
			/**
			 * Lining Definition Style Markup
			 *
			  <dl class="typl8-lining">
			    <dt><b></b></dt>
			    <dd></dd>
			  </dl>
			 *
			 * Extend this object into your markup.
			 *
			 */
			.typl8-lining dt,
			.typl8-lining dd {
			  display: inline;
			  margin: 0; }
			.typl8-lining dt + dt:before,
			.typl8-lining dd + dt:before {
			  content: "\A";
			  white-space: pre; }
			.typl8-lining dd + dd:before {
			  content: ", "; }
			.typl8-lining dd:before {
			  content: ": ";
			  margin-left: -0.2rem; }
			
			/**
			 * Dictionary Definition Style Markup
			 *
			  <dl class="typl8-dictionary-style">
			    <dt><b></b></dt>
			    <dd></dd>
			  </dl>
			 *
			 * Extend this object into your markup.
			 *
			 */
			.typl8-dictionary-style dt {
			  display: inline;
			  counter-reset: definitions; }
			  .typl8-dictionary-style dt + dt:before {
			    content: ", ";
			    margin-left: -0.2rem; }
			.typl8-dictionary-style dd {
			  display: block;
			  counter-increment: definitions; }
			  .typl8-dictionary-style dd:before {
			    content: counter(definitions,decimal) ". "; }
			
			/**
			 * Blockquote Markup
			 *
			    <figure>
			      <blockquote cite="">
			        <p></p>
			      </blockquote>
			      <figcaption>
			        <cite>
			          <small><a href=""></a></small>
			        </cite>
			      </figcaption>
			    </figure>
			 *
			 * Extend this object into your markup.
			 *
			 */
			/**
			 * Pull Quotes Markup
			 *
			  <aside class="typl8-pull-quote">
			    <blockquote>
			      <p></p>
			    </blockquote>
			  </aside>
			 *
			 * Extend this object into your custom stylesheet.
			 *
			 */
			.typl8-pull-quote {
			  position: relative;
			  padding: 1em; }
			  .typl8-pull-quote:before, .typl8-pull-quote:after {
			    height: 1em;
			    opacity: 0.5;
			    position: absolute;
			    font-size: 4em;
			    color: #dc976e; }
			  .typl8-pull-quote:before {
			    content: '“';
			    top: 0;
			    left: 0; }
			  .typl8-pull-quote:after {
			    content: '”';
			    bottom: 0;
			    right: 0; }
			
			/**
			 * Figures Markup
			 *
			  <figure>
			    <figcaption>
			      <strong>Fig. X.X | </strong><cite title=""></cite>
			    </figcaption>
			  </figure>
			 *
			 * Extend this object into your markup.
			 *
			 */
			/**
			 * Footnote Markup : Replace 'X' with your unique number for each footnote
			 *
			  <article>
			    <p><sup><a href="#fn-itemX" id="fn-returnX"></a></sup></p>
			    <footer>
			      <ol class="foot-notes">
			        <li id="fn-itemX"><a href="#fn-returnX">↩</a></li>
			      </ol>
			    </footer>
			  </article>
			 *
			 * Extend this object into your markup.
			 *
			 */
			table.noborder td, table.noborder th, table.noborder tfoot td {
			  border: none !important;
			  background: none !important; }
			
			table {
			  border-collapse: collapse;
			  font-size: 1em;
			  line-height: 1.5em;
			  margin-top: 1.5em;
			  margin-bottom: 1.5em;
			  width: 100%;
			  display: table;
			  text-align: left;
			  margin-top: 3em; }
			
			table + * {
			  margin-top: 3em; }
			
			table caption {
			  font-weight: 600; }
			
			table td, table th, table tfoot td {
			  border: 1px solid #e6e6e6;
			  font-size: 1em;
			  line-height: 1.5em;
			  padding: 10.5px; }
			
			table tr {
			  background: white; }
			
			table tr:nth-child(even) {
			  background: white; }
			
			table tfoot {
			  background: #f2f2f2; }
			
			table th, table tfoot td {
			  font-weight: 600; }
		'''
		return(cssFileBase64.encode('utf-8'))
