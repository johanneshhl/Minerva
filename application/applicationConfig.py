import os
import datetime


PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
SESSION_COOKIE_PATH = '/'

APPLICATION_NAME = u'Minerva'
APPLICATION_OWNER = u'Johannes Hvilsom Larsen'
APPLICATION_VERSION = u'0.1'


if 'DYNO' not in os.environ:
	APPLICATION_MODE = u'localhost'
	DEBUG = True
	PREFERRED_URL_SCHEME = 'http'
	SESSION_COOKIE_DOMAIN = '0.0.0.0'
else:
	APPLICATION_MODE = u'Heroku'
	SERVER_NAME = 'jhvilsom.dk'
	SESSION_COOKIE_DOMAIN = '.jhvilsom.dk'
	SESSION_COOKIE_SECURE = True
	SESSION_COOKIE_NAME = 'herokuSession'
	PREFERRED_URL_SCHEME = 'https'
	DEBUG = False


UPLOAD_FOLDER = 'static/assets'


SECRET_KEY = u'\x89\x15\xbe\x8c\x93\xf0k\xee\x91\xe0\xae\xba\xb3?\xdc\xa9\xe1ns8\xceVe]'

#set up localhost usage
if not os.environ.has_key('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///../test.db'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


del datetime
del os