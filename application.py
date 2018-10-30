from flask import Flask, request, render_template
from flaskext.mysql import MySQL

import json

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# Import configuration for database connection
with open('app-config.json') as config: 
    app_config = json.load(config)

db_config = app_config['database']

mysql = MySQL()

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = db_config['user']
application.config['MYSQL_DATABASE_PASSWORD'] = db_config['password']
application.config['MYSQL_DATABASE_DB'] = db_config['database']
application.config['MYSQL_DATABASE_HOST'] = db_config['host']

#Init db connection and get cursor
mysql.init_app(application)
conn = mysql.connect()
cursor = conn.cursor()
    
# import os

# if 'RDS_HOSTNAME' in os.environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'mysql',
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# cursor = mysql.get_db().cursor()
# cursor = mysql.connect().cursor()
# cur = mysql.connect().cursor()

# add a rule for the index page.
# application.add_url_rule('/', 'index', (lambda: header_text +
#     say_hello() + instructions + footer_text))

@application.route('/')
def users():
	#cursor.execute(''' SELECT * FROM ebdb.test limit 0, 1; ''')
	#rv = cursor.fetchall()
    #print(rv)
	return render_template('home.html')
    #return "<p>Hello World!</p>"
    #print rv
	#return str(rv)

@application.route('/', methods=['POST'])
def my_form_post():
	id = request.form['id']
	first = request.form['fname']
	last = request.form['lname']
	email = request.form['email']
	
	
	query = "INSERT INTO ebdb.test VALUES(%s, %s, %s, %s,NULL);"
	cursor.execute(query, [id, first, last, email])
	conn.commit()
	return render_template('home.html')
    
    #processed_text = text.upper()
    #return processed_text
	
# add a rule when the page is accessed with a name appended to the site
# URL.
# application.add_url_rule('/<username>', 'hello', (lambda username:
#     header_text + say_hello(username) + home_link + footer_text))


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()