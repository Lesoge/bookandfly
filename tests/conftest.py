import pytest

from app import create_app
from scripts.db_setup import create_standard_admin
from dbModel import db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app({'version': 1}, 'flask_testcfg.py', False)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.drop_all()
    create_standard_admin()

    yield db

    db.drop_all()
