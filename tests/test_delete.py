import pytest
from app.db import get_db

def test_delete_entry(client, auth, app):
    """Test deleting an entry."""
    auth.register()
    auth.login()
    
    # Add an entry
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO entries (user_id, text, mood, reflection) VALUES (1, 'Test entry', 'happy', 'Great!')"
        )
        db.commit()
        entry_id = db.execute('SELECT id FROM entries').fetchone()['id']
    
    # Delete the entry
    response = client.post(f'/entries/{entry_id}/delete', follow_redirects=True)
    assert b'Entry deleted successfully!' in response.data
    
    # Verify entry was deleted
    with app.app_context():
        db = get_db()
        entry = db.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
        assert entry is None

def test_delete_requires_login(client, app):
    """Test that deleting requires login."""
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES ('test', 'hash')"
        )
        db.execute(
            "INSERT INTO entries (user_id, text) VALUES (1, 'Test')"
        )
        db.commit()
        entry_id = db.execute('SELECT id FROM entries').fetchone()['id']
    
    response = client.post(f'/entries/{entry_id}/delete')
    assert response.headers['Location'] == '/auth/login'

def test_delete_wrong_user(client, auth, app):
    """Test that user can't delete another user's entry."""
    # User1 creates entry
    auth.register('user1', 'pass1')
    auth.login('user1', 'pass1')
    
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO entries (user_id, text) VALUES (1, 'User1 entry')"
        )
        db.commit()
        entry_id = db.execute('SELECT id FROM entries').fetchone()['id']
    
    auth.logout()
    
    # User2 tries to delete User1's entry
    auth.register('user2', 'pass2')
    auth.login('user2', 'pass2')
    
    response = client.post(f'/entries/{entry_id}/delete')
    assert response.status_code == 403  # Forbidden

def test_delete_nonexistent_entry(client, auth):
    """Test deleting non-existent entry returns 404."""
    auth.register()
    auth.login()
    
    response = client.post('/entries/9999/delete')
    assert response.status_code == 404