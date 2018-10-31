from flask import Flask, request, render_template, jsonify, abort, make_response
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

import json

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# Import configuration for database connection
with open('app-config.json') as config:
	app_config = json.load(config)

db_config = app_config['database']

mysql = MySQL(cursorclass=DictCursor)

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = db_config['user']
application.config['MYSQL_DATABASE_PASSWORD'] = db_config['password']
application.config['MYSQL_DATABASE_DB'] = db_config['database']
application.config['MYSQL_DATABASE_HOST'] = db_config['host']

# Init db connection and get cursor
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


def say_hello(username="World"):
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

# Error handler in case of 404 (can customize this)
# invoked when `abort(404)` called
@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@application.route('/')
def users():
	#cursor.execute(''' SELECT * FROM ebdb.test limit 0, 1; ''')
	#rv = cursor.fetchall()
	# print(rv)
	return render_template('home.html')
	# return "<p>Hello World!</p>"
	# print rv
	# return str(rv)


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
	# return processed_text

# run http://127.0.0.1:5000/api/test/zip/61801
@application.route('/api/test/zip/<int:zipcode>', methods=['GET'])
def getTestJSON(zipcode):
	zipcode = request.args.get('zipcode')
	query = 'SELECT state_code, state_name, county_name, city_name, latitude, longitude, average_temperature, min_monthly_lows, max_monthly_highs FROM temp_zipcode_data WHERE zip_code = %s'
	cursor.execute(query, (zipcode))
	returnedData = cursor.fetchall()
	return jsonify({'data': returnedData})

# Given a zipcode as GET query param, get its information
# run http://127.0.0.1:5000/api/zipcode/info?zipcode=61801
@application.route('/api/zipcode/info', methods=['GET'])
def getInfoForZipcode():
	zipcode = request.args.get('zipcode')
	query = 'SELECT state_code, state_name, county_name, city_name, latitude, longitude, average_temperature, min_monthly_lows, max_monthly_highs FROM temp_zipcode_data WHERE zip_code = %s'
	cursor.execute(query, (zipcode))
	returnedData = cursor.fetchall()
	return jsonify({'data': returnedData})

# Return all zipcodes that have avg temperatures between <low> and <high> inclusive
# run http://127.0.0.1:5000/api/weather/avgTempRange?low=40&high=90
@application.route('/api/weather/avgTempRange', methods=['GET'])
def getZipWithinAvgTemp():
	low = request.args.get('low')
	high = request.args.get('high')

	query = 'SELECT zip_code, average_temperature FROM temp_zipcode_data WHERE average_temperature BETWEEN %s and %s'
	cursor.execute(query, (low, high))
	returnedData = cursor.fetchall()
	return jsonify({'data': returnedData})



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
