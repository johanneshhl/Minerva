 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from functools import wraps
from application import Flask, app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash



def login_required(f):
    @wraps(f)
	
    def decorated_function(*args, **kwargs):
        
        if g.userIsloggedIn == False:

            return redirect(url_for('logUserIn', next=replaceHTTP(request.url), _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))

        return f(*args, **kwargs)
    return decorated_function



def allready_logged_in(f):
    @wraps(f)
	
    def decorated_function(*args, **kwargs):
        
        if g.userIsloggedIn == True:
            return redirect(url_for('index'))

        return f(*args, **kwargs)
    return decorated_function








#needle in haystack
def conatins(input, string):
    if string in input:
        return True
    else:
        return False


def replaceHTTP(url):   
    if conatins(url, app.config['PREFERRED_URL_SCHEME']):
        return url
    else:
        newUrl = url.replace('http', app.config['PREFERRED_URL_SCHEME'])
        return newUrl
