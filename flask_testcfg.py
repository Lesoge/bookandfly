# SQLAlchemy Config
db_ip_and_port = 'localhost:5432'
dbname = 'testbookandflydb'
dbuser = 'admin'
dbpassword = 'admin'
echomode = True
database_url = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = 'FALSE'

# flask config
SECRET_KEY = 'fuifigouigzuftzdtzdtzdztddzrdz'
DEBUG = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# FLASK Security
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = ''
SECURITY_PASSWORD_LENGTH_MIN = 9
SECURITY_PASSWORD_COMPLEXITY_CHECKER = 'zxcvbn'
SECURITY_PASSWORD_CHECK_BREACHED = 'best-effort'

CERT_PATH = 'tests/functional/cert.pem'
KEY_PATH = 'tests/functional/key.pem'

TESTING = True
SERVER_NAME = 'test'
