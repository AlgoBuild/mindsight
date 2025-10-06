import pytest
from flask import g, session
from app.db import get_db

def test_register(client, app):
    """Test user registration."""
    # Test that registration page loads
    assert client.get('/auth/register').status_code == 200
    
    # Test successful registration
    response = client.post(
        '/auth/register',
        data={'username': 'newuser', 'password': 'newpass'}
    )
    assert response.headers['Location'] == '/auth/login'
    
    # Verify user was added to database
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM users WHERE username = 'newuser'"
        ).fetchone() is not None

def test_register_validates_input(client):
    """Test registration input validation."""
    # Test missing username
    response = client.post(
        '/auth/register',
        data={'username': '', 'password': 'test'}
    )
    assert b'Username is required' in response.data
    
    # Test missing password
    response = client.post(
        '/auth/register',
        data={'username': 'test', 'password': ''}
    )
    assert b'Password is required' in response.data

def test_register_duplicate_username(client, auth):
    """Test that duplicate username is rejected."""
    auth.register()
    response = auth.register()
    assert b'already registered' in response.data

def test_login(client, auth):
    """Test user login."""
    # Register a user first
    auth.register()
    
    # Test that login page loads
    assert client.get('/auth/login').status_code == 200
    
    # Test successful login
    response = auth.login()
    assert response.headers['Location'] == '/'
    
    # Verify session has user_id
    with client:
        client.get('/')
        assert session['user_id'] is not None

def test_login_validates_input(client, auth):
    """Test login input validation."""
    auth.register()
    
    # Test wrong username
    response = auth.login('wronguser', 'testpass')
    assert b'Incorrect username' in response.data
    
    # Test wrong password
    response = auth.login('testuser', 'wrongpass')
    assert b'Incorrect password' in response.data

def test_logout(client, auth):
    """Test user logout."""
    auth.register()
    auth.login()
    
    # Test logout clears session
    auth.logout()
    
    with client:
        client.get('/')
        assert 'user_id' not in session