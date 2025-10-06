import os
import tempfile
import pytest
from app import create_app
from app.db import get_db, init_db

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    # Create test app with test database
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test',
    })
    
    # Create the database and load test data
    with app.app_context():
        init_db()
    
    yield app
    
    # Cleanup: close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()

class AuthActions:
    """Helper class for authentication in tests."""
    def __init__(self, client):
        self._client = client
    
    def register(self, username='testuser', password='testpass'):
        """Register a new user."""
        return self._client.post(
            '/auth/register',
            data={'username': username, 'password': password}
        )
    
    def login(self, username='testuser', password='testpass'):
        """Log in a user."""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        """Log out the current user."""
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    """Authentication helper fixture."""
    return AuthActions(client)