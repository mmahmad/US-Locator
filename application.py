from flask import Flask
from flaskext.mysql import MySQL
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

# EB looks for an 'application' callable by default.
application = Flask(__name__)
# MySQL configurations
# application.config['MYSQL_USER'] = 'cs411'
# application.config['MYSQL_PASSWORD'] = 'cs411dbuser'
# application.config['MYSQL_DB'] = 'ebdb'
# application.config['MYSQL_HOST'] = 'aa1enwpis40fd9h.crncuapzhdos.us-west-2.rds.amazonaws.com'

mysql = MySQL()
# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'cs411'
application.config['MYSQL_DATABASE_PASSWORD'] = 'cs411dbuser'
application.config['MYSQL_DATABASE_DB'] = 'ebdb'
application.config['MYSQL_DATABASE_HOST'] = 'aa1enwpis40fd9h.crncuapzhdos.us-west-2.rds.amazonaws.com'
mysql.init_app(application)

# cursor = mysql.get_db().cursor()
# cursor = mysql.connect().cursor()
conn = mysql.connect()
cursor = conn.cursor()
# cur = mysql.connect().cursor()

# add a rule for the index page.
# application.add_url_rule('/', 'index', (lambda: header_text +
#     say_hello() + instructions + footer_text))

@application.route('/')
def users():
    cursor.execute('''SELECT * FROM ebdb.test limit 0, 1;''')
    rv = cursor.fetchall()
    print(rv)
    return "<p>Hello World!</p>"
    # print rv
    # return str(rv)

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