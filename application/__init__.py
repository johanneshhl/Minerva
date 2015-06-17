 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from flask import Flask, send_file, abort, Response, jsonify, request, redirect, url_for, session, escape, render_template, g, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.assets import Environment, Bundle

from datetime import datetime


app = Flask(__name__)
app.config.from_object('application.applicationConfig')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
assets = Environment(app)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# Find filer der skal minifierser
js = Bundle('assets/jquery.min.js','assets/bifrost.js', 'assets/main.js', filters='jsmin', output='gen/packed.js')
css = Bundle('assets/main.css',  filters='cssmin', output='gen/packed.css')

# Hent de minifiserde filer
assets.register('js_all', js)
assets.register('css_all', css)

import application.database

import application.controlers
import application.models





app.logger.info('Starting : {0}\nBy: {1}\nVersion: {2}\nMode: {3}'.format(app.config['APPLICATION_NAME'],
																		  app.config['APPLICATION_OWNER'],
																		  app.config['APPLICATION_VERSION'],
																		  app.config['APPLICATION_MODE']))


db.create_all()