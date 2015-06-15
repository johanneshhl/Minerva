 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from functools import wraps
from application import Flask, app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash



def login_required(f):
    @wraps(f)

    '''
        Hvis brugeren er ikke logget ind, 
        så videre send brugen til login siden og
        tilføj et parameter med den efterspurgte side.
    '''
	
    def decorated_function(*args, **kwargs):
        
        if g.userIsloggedIn == False: #hvis brugren ikke er logget ind

            #vidre send til LogUserIn funktionen, med HTTPS
            return redirect(url_for('logUserIn', next=replaceHTTP(request.url), _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))

        return f(*args, **kwargs)
    return decorated_function



def allready_logged_in(f):
    @wraps(f)

    '''
        Er siden allerede logget ind så send brugen til forsiden
    
    '''
	
    def decorated_function(*args, **kwargs):
        
        if g.userIsloggedIn == True: #hvis brugren er logget ind
            return redirect(url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))

        return f(*args, **kwargs)
    return decorated_function




#gammle kode, der omskrev url'en til https
def replaceHTTP(url):   
    if conatins(url, app.config['PREFERRED_URL_SCHEME']):
        return url
    else:
        newUrl = url.replace('http', app.config['PREFERRED_URL_SCHEME'])
        return newUrl
