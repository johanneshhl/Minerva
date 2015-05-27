 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from flask import Flask, send_file, abort, request, redirect, url_for, session, escape, render_template, g, flash
from flask.ext.heroku import Heroku 
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
js = Bundle('js/jquery.min.js', 'js/bifrost.js', 'js/bootstrap.min.js', 'js/cookieAlert.js', 'js/main.js', filters='jsmin', output='gen/packed.js')
css = Bundle('css/bootstrap.css', 'css/style.css',  filters='cssmin', output='gen/packed.css')

# Hent de minifiserde filer
assets.register('js_all', js)
assets.register('css_all', css)


import application.controlers
import application.models
import application.views



db.create_all()