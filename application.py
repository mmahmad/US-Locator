from flask import Flask, request, render_template, jsonify, abort, make_response
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import hashlib, uuid
from passlib.hash import sha256_crypt

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

############################################ APIs Begin ################################################################################

# TODO: Use POST instead of GET
# create user
@application.route('/api/user/new', methods=['GET'])
def createNewUser():
	username = request.args.get('username')
	password = request.args.get('password')
	# salt = uuid.uuid4().hex
	# hashed_password = hashlib.sha512(password + salt).hexdigest()
	# encrypted_passwd = sha256_crypt.encrypt(password)

	# check if username already exists in db

	query = 'SELECT username FROM users WHERE username = %s'
	cursor.execute(query, (username))
	
	returnedData = cursor.fetchall()
	if len(returnedData) > 0:
		# user already exists, so return error
		return jsonify({'error': 'Username already exists.'})
	else:
		query = 'INSERT INTO users(username, passwd) VALUES (%s, %s)'
		# cursor.execute(query, (username, encrypted_passwd))
		cursor.execute(query, (username, password))
		conn.commit()
		return jsonify({'success': 'User created successfully'})


# User login
@application.route('/api/user/login', methods=['GET'])
def userLogin():
	username = request.args.get('username')
	password = request.args.get('password')
	# salt = uuid.uuid4().hex
	# hashed_password = hashlib.sha512(password + salt).hexdigest()
	# encrypted_passwd = sha256_crypt.encrypt(password)
	# print("encrypted password is: ")
	# print(encrypted_passwd)

	# 

	query = 'SELECT username FROM users WHERE username = %s AND passwd=%s'
	cursor.execute(query, (username, password))
	returnedData = cursor.fetchall()
	if len(returnedData) > 0:
		# return jsonify({'success': 'Authentication successful'})
		# check if pwds match
		# print("returned data:")
		# print(returnedData)
		# dbpasswd = returnedData[0]['passwd']
		# print('dbpasswd: ')
		# print(dbpasswd)

		# if sha256_crypt.verify(encrypted_passwd, dbpasswd):
		# 	# verified, so authenticated
		# 	return jsonify({'success': 'Authentication successful'})
		# else:
		# 	return jsonify({'error': 'Invalid username or password'})

		return jsonify({'success': 'Authentication successful'})

	else:
		return jsonify({'error': 'Invalid username or password'})

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

# Return all zipcodes in a given city/county/state. 2 GET params required
# run http://127.0.0.1:5000/api/zipcodes/region?region=state&region_value=illinois
@application.route('/api/zipcodes/region', methods=['GET'])
def getZipcodesInCity():
	region = request.args.get('region')
	region_value = request.args.get('region_value')

	if (region and region_value):
		if (region == 'city'):
			query = 'SELECT zip_code FROM temp_zipcode_data WHERE city_name = %s'
		elif (region == 'county'):
			query = 'SELECT zip_code FROM temp_zipcode_data WHERE county_name = %s'
		elif (region == 'state'):
			query = 'SELECT zip_code FROM temp_zipcode_data WHERE state_name = %s'

		cursor.execute(query, (region_value))
		returnedData = cursor.fetchall()
		return jsonify({'data': returnedData})
	else:
		abort(404)

############################################################ APIs End #####################################################################

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
