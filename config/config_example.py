#SQLAlchemy Config
db_ip_and_port = ''
dbname =  ''
dbuser = ''
dbpassword = ''
database_url = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

#flask config
SECRET_KEY = ''
DEBUG = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'strict'
SESSION_COOKIE_HTTPONLY = True
#FLASK Security
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = ''
SECURITY_PASSWORD_LENGTH_MIN = 9
SECURITY_PASSWORD_COMPLEXITY_CHECKER = 'zxcvbn'
SECURITY_PASSWORD_CHECK_BREACHED = 'best-effort'

CERT_PATH = 'cert.pem'
KEY_PATH = 'ca-key.pem'

LOGIN_ATTEMPTS_BEFORE_LOCK = 10
APP_IP = '127.0.0.1'