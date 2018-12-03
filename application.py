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

#current_login_id = 0


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
	return render_template('login.html', logged_in = 0, current_login_id = 0)
	
	
@application.route('/home', methods=['POST'])
def home():
	if(request.form.get('login_id')):
		current_login_id = request.form['login_id']
	logged_in = 1
	return render_template('home.html', logged_in = logged_in, current_login_id = current_login_id)



@application.route('/login')
def login_page():
	return render_template('login.html')

	
@application.route('/create_acc', methods=['POST'])
def createAcc():
	user = request.form['userNew']
	password = request.form['passwordNew']
	
	query = 'SELECT username FROM users WHERE username = %s'
	cursor.execute(query, (user))
	
	returnedData = cursor.fetchall()
	
	if len(returnedData) > 0:
		# user already exists, so return error
		return jsonify({'error': 'Username already exists.'})
		
	
	query1 = "SELECT max(id) FROM users"
	cursor.execute(query1)
	
	max_id = cursor.fetchall()
	max_id = max_id[0]['max(id)']
	
	new_id = max_id + 1
	
	query2 = "INSERT INTO ebdb.users VALUES(%s, %s, %s)"
	cursor.execute(query2, [new_id, user, password])
	conn.commit()
	
	current_login_id = new_id
	logged_in = 1
	return render_template('home.html', logged_in = logged_in, current_login_id = current_login_id)
	
# User login
@application.route('/signin', methods=['POST'])
def signin():
	username = request.form['user']
	password = request.form['password']

	query = 'SELECT id, username FROM users WHERE username = %s AND passwd=%s'
	cursor.execute(query, (username, password))
	returnedData = cursor.fetchall()
	
	if len(returnedData) > 0:
		#return jsonify(returnedData[0]['id'])
		current_login_id = returnedData[0]['id']
		logged_in = 1;
		return render_template('home.html', logged_in = logged_in, current_login_id = current_login_id)

	else:
		return jsonify({'error': 'Invalid username or password'})

@application.route('/results', methods=['POST'])
def my_form_post():
	#id = request.form['id']
	#first = request.form['fname']
	#last = request.form['lname']
	#email = request.form['email']
	
	#city = request.form['city']
	#state = request.form['state']
	

	#query = "INSERT INTO ebdb.test VALUES(%s, %s, %s, %s,NULL);"
	#cursor.execute(query, [id, first, last, email])
	#conn.commit()
	
	low = 0
	high = 75
	
	
	min_house = 0
	max_house = 7526600
	
	min_crime = 0
	max_crime = 994
	
	current_login_id = 0
	
	if(request.form.get('login_id')):
		current_login_id = request.form['login_id']
	
	
	# if(request.form.get('temp_check')):
	# 	low = request.form['min_temp']
	# 	high = request.form['max_temp']
		
	# if(request.form.get('house_check')):
	# 	min_house = request.form['min_house']
	# 	max_house = request.form['max_house']
		
	# if(request.form.get('crime_check')):
	# 	min_crime = request.form['min_crime']
	# 	max_crime = request.form['max_crime']

	
	# query = 'SELECT case WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN "1" ELSE "0" END as is_favorite , ws.zipcode_id, z.zipcode, z.latitude, z.longitude, z.county_name, cd.violent_crimes_total, z.state, ws.avg_temp, hs.median_house_price FROM home_stats hs JOIN weather_stats ws ON hs.zipcode_id = ws.zipcode_id JOIN zipcodes z ON z.id = ws.zipcode_id JOIN county_crime_data cd ON z.county_name = cd.county WHERE avg_temp BETWEEN %s and %s AND median_house_price BETWEEN %s and %s and violent_crimes_total BETWEEN %s and %s'
	# cursor.execute(query, (current_login_id, low, high, min_house, max_house, min_crime, max_crime))
	# returnedData = cursor.fetchall()
	# print('length of data:')
	# print(len(returnedData))

	# returnedData = json.dumps(returnedData)
	
	# return render_template('result.html', returnedData = returnedData, current_login_id = current_login_id)

	projections = [
		"CASE WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN '1' ELSE '0' END as is_favorite",
		"z.id",
		"z.zipcode",
		"z.latitude",
		"z.longitude"
	]

	joins = [
		"zipcodes z "
	]
	# requiresWeather = False
	# requiresHousePrice = False
	# requiresCrime = False

	conditionsRequired = 0
	conditions = []
	
	if(request.form.get('temp_check')):
		low = request.form['min_temp']
		high = request.form['max_temp']
		if low and high:
			requiresWeather = True
			# query += "JOIN weather_stats w ON z.id=w.zipcode_id "
			joins.append("JOIN weather_stats w ON z.id=w.zipcode_id ")
			conditionsRequired += 1
			condition = "w.avg_temp BETWEEN {} and {} ".format(low, high)
			projections.append("w.avg_temp as Average_Temperature")
			conditions.append(condition)
		else:
			abort(404)

	if(request.form.get('crime_check')):
		min_crime = request.form['min_crime']
		max_crime = request.form['max_crime']
		if max_crime and min_crime:
			requiresCrime = True
			# query += "JOIN county_crime_data ccd ON z.county_name=ccd.county "
			joins.append("JOIN county_crime_data ccd ON z.county_name=ccd.county ")
			conditionsRequired += 1
			condition = "ccd.violent_crimes_total BETWEEN {} and {} ".format(min_crime, max_crime)
			projections.append("ccd.violent_crimes_total as Total_Violent_Crimes")
			conditions.append(condition)
		else:
			abort(404)
		
	if(request.form.get('house_check')):
		min_house = request.form['min_house']
		max_house = request.form['max_house']
		if min_house and max_house:
			requiresHousePrice = True
			# query += "JOIN home_stats hs ON z.id=hs.zipcode_id "
			joins.append("JOIN home_stats hs ON z.id=hs.zipcode_id ")
			conditionsRequired += 1
			condition = "hs.median_house_price BETWEEN {} and {} ".format(min_house, max_house)
			projections.append("hs.median_house_price as Median_House_Price")
			conditions.append(condition)
		else:
			abort(404)

	query = "SELECT "
	for i in range(0, len(projections)):
		if i == (len(projections) - 1):
			query += projections[i]
		else:
			query += projections[i] + ","
	
	query += " FROM "

	for join in joins:
		query += join

	# start adding conditions
	query += " WHERE "

	if len(conditions) == 1:
		# just one condition
		query += conditions[0] + ';'
	elif len(conditions) > 1:
		# separated by "and"
		for i in range(0, len(conditions)):
			if i == (len(conditions) - 1):
				query += " AND " + conditions[i] + ";"
			elif i==0:
				query += conditions[i]
			else:
				query += " AND " + conditions[i]
	else:
		# No condition provided. Should never reach this part of code
		print("ERROR! NO CONDITION PROVIDED!")

	
	# query = 'SELECT case WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN "1" ELSE "0" END as is_favorite , ws.zipcode_id, z.zipcode, z.latitude, z.longitude, z.county_name, cd.violent_crimes_total, z.state, ws.avg_temp, hs.median_house_price FROM home_stats hs JOIN weather_stats ws ON hs.zipcode_id = ws.zipcode_id JOIN zipcodes z ON z.id = ws.zipcode_id JOIN county_crime_data cd ON z.county_name = cd.county WHERE avg_temp BETWEEN %s and %s AND median_house_price BETWEEN %s and %s and violent_crimes_total BETWEEN %s and %s'

	print("final query:")
	print(query)
	# cursor.execute(query, (current_login_id, low, high, min_house, max_house, min_crime, max_crime))
	cursor.execute(query, (current_login_id))
	returnedData = cursor.fetchall()
	print('length of data:')
	print(len(returnedData))
	returnedData = json.dumps(returnedData)
	
	return render_template('result.html', returnedData = returnedData, current_login_id = current_login_id)
	
	
@application.route('/view_favorites', methods=['POST'])
def view_favorites():
	if(request.form.get('login_id')):
		current_login_id = request.form['login_id']
	# query = 'SELECT case WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN "1" ELSE "0" END as is_favorite, ws.zipcode_id, z.zipcode, z.latitude, z.longitude, z.county_name, z.state, ws.avg_temp, hs.median_house_price FROM home_stats hs JOIN weather_stats ws ON hs.zipcode_id = ws.zipcode_id JOIN zipcodes z ON z.id = ws.zipcode_id WHERE z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id)' 
	query = 'SELECT case WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN "1" ELSE "0" END as is_favorite, z.id, z.zipcode, z.latitude, z.longitude, z.county_name, z.state, IFNULL(ws.avg_temp,"N/A") as average_temparature, IFNULL(hs.median_house_price,"N/A") as median_house_price FROM favorites f LEFT JOIN zipcodes z on z.id=f.zipcode_id LEFT JOIN home_stats hs on z.id=hs.zipcode_id LEFT JOIN weather_stats ws ON z.id = ws.zipcode_id WHERE f.user_id=%s;'
	cursor.execute(query, (current_login_id, current_login_id))
	returnedData = cursor.fetchall()
	
	print('length of data:')
	print(len(returnedData))
	returnedData = json.dumps(returnedData)
	
	return render_template('result.html', returnedData = returnedData, current_login_id = current_login_id)
	
@application.route('/county_tables', methods=['POST'])
def county_tables():

	current_login_id = 0
	
	if(request.form.get('login_id')):
		current_login_id = request.form['login_id']
		
	min_crime = 0
	max_crime = 994
	
	if(request.form.get('crime_check')):
		min_crime = request.form['min_crime']
		max_crime = request.form['max_crime']
		
	query = 'SELECT cd.county, cd.violent_crimes_total FROM county_crime_data cd WHERE violent_crimes_total BETWEEN %s and %s'
	
	cursor.execute(query, (min_crime, max_crime))
	returnedData = cursor.fetchall()
	
	returnedData = json.dumps(returnedData)
	print('length of data:')
	print(len(returnedData))
	
	
	return render_template('county.html', returnedData = returnedData, current_login_id = current_login_id)
	
@application.route('/county_zipcodes', methods=['GET'])
def county_zipcodes():

		current_login_id = 0
		if(request.form.get('userId')):
			current_login_id = request.form['userId']
		
		countyName = request.args.get('countyName')
		#query = 'SELECT case WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN "1" ELSE "0" END as is_favorite , ws.zipcode_id, z.zipcode, z.latitude, z.longitude, z.county_name, z.state, ws.avg_temp, hs.median_house_price FROM home_stats hs JOIN weather_stats ws ON hs.zipcode_id = ws.zipcode_id JOIN zipcodes z WHERE z.county_name = %s'
		query = 'SELECT case WHEN z.id IN (SELECT f.zipcode_id FROM favorites f WHERE f.user_id=%s and f.zipcode_id=z.id) THEN "1" ELSE "0" END as is_favorite, z.zipcode, z.latitude, z.longitude FROM zipcodes z WHERE z.county_name = %s'
	
	
		cursor.execute(query, (current_login_id, countyName))
		
		returnedData = cursor.fetchall()
		print('length of data:')
		print(len(returnedData))
		
		returnedData = json.dumps(returnedData)
		
		
		return render_template('result.html', returnedData = returnedData, current_login_id = current_login_id)
		
		
# @application.route('/favorites', methods=['POST', 'GET', 'PUT', 'DELETE'])
# def favorite():
# 	# Add to favorites list
# 	if request.method == 'GET':
# 		zipcodeId = request.args.get('zipcodeId')
# 		userId = request.args.get('userId')	
# 		query = 'INSERT INTO favorites(user_id, zipcode_id) VALUES (%s, %s)'
# 		cursor.execute(query, (userId, zipcodeId))
# 		conn.commit()
# 		return render_template('home.html')

############################################ APIs Begin ################################################################################

# TODO: Use POST instead of GET
# create user
@application.route('/api/user/create', methods=['POST'])
def createNewUser():
	username = request.form.get('username')
	password = request.form.get('password')
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
@application.route('/api/user/login', methods=['POST'])
def userLogin():
	username = request.form.get('username')
	password = request.form.get('password')
	# salt = uuid.uuid4().hex
	# hashed_password = hashlib.sha512(password + salt).hexdigest()
	# encrypted_passwd = sha256_crypt.encrypt(password)
	# print("encrypted password is: ")
	# print(encrypted_passwd)

	# 

	query = 'SELECT id, username FROM users WHERE username = %s AND passwd=%s'
	cursor.execute(query, (username, password))
	returnedData = cursor.fetchall()
	print(returnedData)
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

		return jsonify({'success': 'Authentication successful', 'userId': returnedData[0]['id']})

	else:
		return jsonify({'error': 'Invalid username or password'})

@application.route('/api/user/favorites', methods=['POST', 'GET', 'PUT', 'DELETE'])
def addFavorite():
	# Add to favorites list
	if request.method == 'POST':
		userId = request.form.get('userId')
		zipcodeId = request.form.get('zipcodeId')

		query = 'INSERT INTO favorites(user_id, zipcode_id) VALUES (%s, %s)'
		cursor.execute(query, (userId, zipcodeId))
		conn.commit()
		return jsonify({'success': 'Zipcode added to favorites'})

	# Get favorites list
	elif request.method == 'GET':
		userId = request.args.get('userId')

		query = 'SELECT f.id, z.zipcode FROM zipcodes z JOIN favorites f on f.zipcode_id=z.id WHERE f.user_id=%s'
		cursor.execute(query, (userId))
		returnedData = cursor.fetchall()
		return jsonify({'data': returnedData})

	# Update favorites list
	elif request.method == 'PUT':
		favoritesId = request.args.get('favoritesId')
		newZipcodeId = request.args.get('newZipcodeId')

		query = 'UPDATE favorites SET zipcode_id=%s WHERE id=%s'
		cursor.execute(query, (newZipcodeId, favoritesId))
		conn.commit()
		return jsonify({'success': 'Favorite zipcode updated'})

	elif request.method == 'DELETE':
		# favoritesId = request.args.get('favoritesId')

		userId = request.args.get('userId')
		zipcodeId = request.args.get('zipcodeId')
		
		query = 'DELETE FROM favorites WHERE user_id=%s AND zipcode_id=%s'
		cursor.execute(query, (userId, zipcodeId))
		conn.commit()
		return jsonify({'success': 'Zipcode deleted from favorites list'})

# run http://127.0.0.1:5000/api/test/zip/61801
# @application.route('/api/test/zip/<int:zipcode>', methods=['GET'])
# def getTestJSON(zipcode):
# 	zipcode = request.args.get('zipcode')
# 	query = 'SELECT state_code, state_name, county_name, city_name, latitude, longitude, average_temperature, min_monthly_lows, max_monthly_highs FROM temp_zipcode_data WHERE zip_code = %s'
# 	cursor.execute(query, (zipcode))
# 	returnedData = cursor.fetchall()
# 	return jsonify({'data': returnedData})

# Given a zipcode as GET query param, get its information
# run http://127.0.0.1:5000/api/zipcode/info?zipcode=61801
@application.route('/api/zipcode/info', methods=['GET'])
def getInfoForZipcode():
	zipcode = request.args.get('zipcode')
	# query = 'SELECT state_code, state_name, county_name, city_name, latitude, longitude, average_temperature, min_monthly_lows, max_monthly_highs FROM temp_zipcode_data WHERE zip_code = %s'
	query = 'SELECT z.state as state_name, z.county_name, c.name as city_name, z.latitude, z.longitude, w.avg_temp, w.min_monthly_lows, w.max_monthly_highs, th.median_house_price, th.population_density FROM zipcodes z JOIN cities c ON z.city_id=c.id JOIN weather_stats w ON z.id=w.zipcode_id JOIN temp_house_data th ON z.zipcode=th.zipcode WHERE z.zipcode = %s'
	cursor.execute(query, (zipcode))
	returnedData = cursor.fetchall()
	return jsonify({'data': returnedData})

# Given a state, find all the cities in it
@application.route('/api/list/cities', methods=['GET'])
def getListOfCitiesGivenState():
	state = request.args.get('state')
	query = 'SELECT id, name FROM cities WHERE state = %s;'
	cursor.execute(query, (state))
	returnedData = cursor.fetchall()
	return jsonify({'data': returnedData})

# Return all zipcodes that have avg temperatures between <low> and <high> inclusive
# run http://127.0.0.1:5000/api/weather/avgTempRange?low=40&high=90
@application.route('/api/weather/avgTempRange', methods=['GET'])
def getZipWithinAvgTemp():
	low = request.args.get('low')
	high = request.args.get('high')

	# query = 'SELECT zip_code, average_temperature, county_name, city_name, state_name FROM temp_zipcode_data WHERE average_temperature BETWEEN %s and %s'
	query = 'SELECT z.zipcode, w.avg_temp, z.county_name, c.name as city_name, z.state as state_name FROM zipcodes z JOIN cities c ON z.city_id=c.id JOIN weather_stats w ON z.id=w.zipcode_id WHERE w.avg_temp BETWEEN %s and %s'
	cursor.execute(query, (low, high))
	returnedData = cursor.fetchall()
	return jsonify({'data': returnedData})

# Get aggregated weather information per state
@application.route('/api/weather/weatherPerState', methods=['GET'])
def getWeatherPerState():

	query = 'select z.state, w.avg_temp, w.min_monthly_lows, w.max_monthly_highs from zipcodes z join weather_stats w on z.id=w.zipcode_id group by z.state'
	cursor.execute(query)
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
			# query = 'SELECT zip_code FROM temp_zipcode_data WHERE city_name = %s'
			query = 'SELECT z.zipcode, c.name as city_name FROM zipcodes z JOIN cities c ON z.city_id=c.id WHERE c.name = %s'
		elif (region == 'county'):
			# query = 'SELECT zip_code FROM temp_zipcode_data WHERE county_name = %s'
			query = 'SELECT z.zipcode, z.county_name FROM zipcodes z WHERE z.county_name = %s'
		elif (region == 'state'):
			query = 'SELECT z.zipcode, z.state as state_name FROM zipcodes z WHERE z.state = %s'
		else:
			abort(404)

		cursor.execute(query, (region_value))
		returnedData = cursor.fetchall()
		return jsonify({'data': returnedData})
	else:
		abort(404)

# Get all locations if the given median housing price is satisfied
# SQL INJECTION POSSIBLE HERE!!!!!!!!!!
@application.route('/api/zipcodes/housing', methods=['GET'])
def getHousePrices():

	operator1 = request.args.get('operator1')
	houseprice1 = request.args.get('houseprice1')

	sqlOperator1 = None

	query = 'SELECT z.zipcode, z.latitude, z.longitude, hs.median_house_price FROM home_stats hs JOIN zipcodes z on hs.zipcode_id = z.id WHERE median_house_price '

	if operator1 == 'lessThan':
		query += '< '
	elif operator1 == 'greaterThan':
		query += '> '
	elif operator1 == 'equalTo':
		query += '= '
	elif operator1 == 'equalToOrGreaterThan':
		query += '>= '
	elif operator1 == 'lessThanOrEqualTo':
		query += '<= '
	else:
		return jsonify({'error': 'Supported operators are: lessThan, greaterThan, equalTo, equalToOrGreaterThan, lessThanOrEqualTo'})

	print('sqlOperator1:')
	print(sqlOperator1)
	
	if houseprice1:
		query += str(houseprice1)
		cursor.execute(query)
		# cursor.execute(query)
		returnedData = cursor.fetchall()
		return jsonify({'data': returnedData})
	else:
		return jsonify({'error': 'Supported operators are: lessThan, greaterThan, equalTo, equalToOrGreaterThan, lessThanOrEqualTo'})

# Given a zipcode, get that zip's county's crime info
@application.route('/api/zipcodes/crime', methods=['GET'])
def getCountyCrimeGivenZip():
	zipcode = request.args.get('zipcode')
	query = 'SELECT z.zipcode, z.county_name, ccd.violent_crimes_total, ccd.murders, ccd.rapes, ccd.robberies, ccd.assaults, ccd.burglaries, ccd.larceny_thefts, ccd.vehicle_thefts FROM zipcodes z JOIN county_crime_data ccd ON z.county_name=ccd.county WHERE z.zipcode=%s;'
	cursor.execute(query, (zipcode))
	returnedData = cursor.fetchall()
	if (len(returnedData) > 1):
		returnedData = returnedData[1]
	return jsonify({'data': returnedData})




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
