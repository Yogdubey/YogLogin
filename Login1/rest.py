import pymysql
from app import app
#from db import mysql
import mysql.connector
from flask import jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import closing
		
@app.route('/')
def home():
	if 'username' in session:
		username = session['username']
		return jsonify({'message' : 'You are already logged in', 'username' : username})
	else:
		resp = jsonify({'message' : 'Unauthorized'})
		resp.status_code = 401
		return resp

@app.route('/login', methods=['POST'])
def login():
	
	print("1")
	print("2")
	try:
		_json = request.json
		_username = _json['username']
		_password = _json['password']
		print("3")
		# validate the received values
		with closing(mysql.connect()) as conn:
			with closing(conn.cursor()) as cursor:
				_hashed_password = generate_password_hash(_password)
				cursor.callproc('registeruser',(username, password))
				data = cursor.fetchall()
		if _username and _password:
		#check user exists
			print("4")			
			conn = mysql.connector.connect()
			print("5")
			cursor = conn.cursor()
		#cursor = mysql.connection.cursor()
			
			mysql = "SELECT * FROM user WHERE username=%s"
			sql_where = (_username,)
			
			cursor.execute(mysql, mysql_where)
			row = cursor.fetchone()
			
		if row:
			if check_password_hash(row[2], _password):
				session['username'] = row[1]
				cursor.close()
				conn.close()
				return jsonify({'message' : 'You are logged in successfully'})
			else:
				resp = jsonify({'message' : 'Bad Request - invalid password'})
				resp.status_code = 400
				return resp
		else:
			resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
			resp.status_code = 400
			return resp

	except Exception as e:
		print(e)
		#cursor.close()
		#conn.close()
		return 'ok'
	#finally:
	#	if cursor and conn:
			#cursor.close()
			#conn.close()
		
@app.route('/logout')
def logout():
	if 'username' in session:
		session.pop('username', None)
	return jsonify({'message' : 'You successfully logged out'})
		
if __name__ == "__main__":
    app.run(debug = True)