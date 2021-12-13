# SQLAlchemy Test-Config
# THIS IS A TEST CONFIG DO NOT USE
db_ip_and_port = 'localhost:5432'
dbname = 'testbookandflydb'
dbuser = 'admin'
dbpassword = 'admin'
database_url = 'postgresql+psycopg2://' + dbuser + ':' + dbpassword + '@' + db_ip_and_port + '/' + dbname
SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask config
SECRET_KEY = 'fuifigouigzuftzdtzdtzdztddzrdz'
DEBUG = False
SESSION_COOKIE_SECURE = True

# FLASK Security
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = ''
SECURITY_PASSWORD_LENGTH_MIN = 9
SECURITY_PASSWORD_COMPLEXITY_CHECKER = 'zxcvbn'
SECURITY_PASSWORD_CHECK_BREACHED = 'best-effort'

CERT_NAME = 'tests/functional/cert.pem'
KEY_NAME = 'tests/functional/key.pem'

TESTING = True
SERVER_NAME = 'test'

LOGIN_ATTEMPTS_BEFORE_LOCK = 10
WTF_CSRF_ENABLED = False
