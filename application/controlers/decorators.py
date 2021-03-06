 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from functools import wraps
from application import Flask, app, request, redirect, escape, session, url_for, db, bcrypt, render_template, g, flash



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        '''
            Hvis brugeren er ikke logget ind, 
            så videre send brugen til login siden og
            tilføj et parameter med den efterspurgte side.
        '''
            
        if g.userIsloggedIn == False: #hvis brugren ikke er logget ind

            #vidre send til LogUserIn funktionen, med HTTPS
            return redirect(url_for('logUserIn', next=replaceHTTP(request.url), _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))

        return f(*args, **kwargs)
    return decorated_function



def allready_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        '''
            Er siden allerede logget ind så send brugen til forsiden
        
        '''
        
        if g.userIsloggedIn == True: #hvis brugren er logget ind
            return redirect(url_for('index', _external=True, _scheme=app.config['PREFERRED_URL_SCHEME']))

        return f(*args, **kwargs)
    return decorated_function



