import os
import datetime


PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
SESSION_COOKIE_PATH = '/'
APPLICATION_NAME = u'Minerva'

if 'DYNO' not in os.environ:
	DEBUG = True
	PREFERRED_URL_SCHEME = 'http'
	SESSION_COOKIE_DOMAIN = '0.0.0.0'
else:
	SERVER_NAME = 'jhvilsom.dk'
	SESSION_COOKIE_DOMAIN = '.jhvilsom.dk'
	SESSION_COOKIE_SECURE = True
	SESSION_COOKIE_NAME = 'herokuSession'
	PREFERRED_URL_SCHEME = 'https'
	DEBUG = False


UPLOAD_FOLDER = 'static/assets'


SECRET_KEY = '\xf1\xc7\x15\xf6:\xca\xde=\xef\xedG!\xd3\x19\x12\x00_\x15\xc8\xe3\x9d\xc0<Z'

#set up localhost usage
if not os.environ.has_key('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///../test.db'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


del datetime
del os