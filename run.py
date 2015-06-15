 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from application import app


'''
	Start program på port 33507 - Heroku's standart port

'''

if __name__ == '__main__':
    import os  
    port = int(os.environ.get('PORT', 33507)) 
    app.run(host='0.0.0.0', port=port)
