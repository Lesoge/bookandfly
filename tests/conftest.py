import pytest

from app import create_app
from scripts.db_setup import create_standard_admin
from dbModel import db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(logger_config, 'config/flask_testcfg.py', False)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.drop_all()
    create_standard_admin('admin', 'admin@admin.de', '1234')

    yield db

    db.drop_all()


logger_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'wsgi': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'console']
    }
}
