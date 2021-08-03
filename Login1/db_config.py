from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root@1234567'
app.config['MYSQL_DB'] = 'Login'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app()