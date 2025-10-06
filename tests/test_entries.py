import pytest
from app.db import get_db

def test_add_entry_requires_login(client):
    """Test that adding entry requires login."""
    response = client.get('/entries/add')
    # Should redirect to login
    assert response.headers['Location'] == '/auth/login'

def test_add_entry_page_loads(client, auth):
    """Test that add entry page loads when logged in."""
    auth.register()
    auth.login()
    
    response = client.get('/entries/add')
    assert response.status_code == 200
    assert b'New Journal Entry' in response.data

def test_add_entry_saves_to_database(client, auth, app):
    """Test that adding entry saves to database."""
    auth.register()
    auth.login()
    
    # Add an entry
    response = client.post(
        '/entries/add',
        data={'text': 'Test journal entry'}
    )
    
    # Should redirect to list page
    assert response.headers['Location'] == '/entries/list'
    
    # Verify entry was saved
    with app.app_context():
        db = get_db()
        entry = db.execute('SELECT * FROM entries').fetchone()
        assert entry is not None
        assert entry['text'] == 'Test journal entry'

def test_add_entry_validates_input(client, auth):
    """Test that empty entry is rejected."""
    auth.register()
    auth.login()
    
    response = client.post(
        '/entries/add',
        data={'text': ''}
    )
    assert b'Journal entry text is required' in response.data

def test_list_entries_requires_login(client):
    """Test that viewing entries requires login."""
    response = client.get('/entries/list')
    assert response.headers['Location'] == '/auth/login'

def test_list_entries_shows_user_entries(client, auth, app):
    """Test that list shows only logged-in user's entries."""
    # Create two users
    auth.register('user1', 'pass1')
    auth.login('user1', 'pass1')
    
    # User1 adds an entry
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO entries (user_id, text, mood, reflection) VALUES (1, 'User1 entry', 'happy', 'Great!')"
        )
        db.commit()
    
    auth.logout()
    
    # User2 registers and logs in
    auth.register('user2', 'pass2')
    auth.login('user2', 'pass2')
    
    # User2 should not see User1's entry
    response = client.get('/entries/list')
    assert b'User1 entry' not in response.data

def test_list_entries_empty_state(client, auth):
    """Test empty state message when no entries."""
    auth.register()
    auth.login()
    
    response = client.get('/entries/list')
    assert b'No entries yet' in response.data