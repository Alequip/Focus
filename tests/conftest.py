import pytest
from app import create_app
from app.models import db as _db

@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app('development')
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with _app.app_context():
        _db.create_all()
        yield _app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Create a database for the tests."""
    return _db
