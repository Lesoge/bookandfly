#SQLAlchemy Config
db_ip_and_port = ''
dbname =  ''
dbuser = ''
dbpassword = ''
echomode = ''
database_url = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_ECHO = True

#flask config
SECRET_KEY = ''
DEBUG = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'

#FLASK Security
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = ''
SECURITY_PASSWORD_LENGTH_MIN = 9
SECURITY_PASSWORD_COMPLEXITY_CHECKER = 'zxcvbn'
SECURITY_PASSWORD_CHECK_BREACHED = 'best-effort'
