import pytest
from unittest.mock import patch
from app.db import get_db

@patch('app.entries.call_gemini_api')
def test_add_entry_calls_gemini(mock_gemini, client, auth, app):
    """Test that adding entry calls Gemini API."""
    auth.register()
    auth.login()
    
    # Mock Gemini response
    mock_gemini.return_value = {
        'mood': 'happy',
        'reflection': 'You seem positive today!'
    }
    
    # Add entry
    client.post(
        '/entries/add',
        data={'text': 'Today was amazing!'}
    )
    
    # Verify Gemini was called
    mock_gemini.assert_called_once_with('Today was amazing!')

@patch('app.entries.call_gemini_api')
def test_gemini_response_saved_to_db(mock_gemini, client, auth, app):
    """Test that Gemini response is saved to database."""
    auth.register()
    auth.login()
    
    # Mock Gemini response
    mock_gemini.return_value = {
        'mood': 'excited',
        'reflection': 'Keep up the enthusiasm!'
    }
    
    # Add entry
    client.post(
        '/entries/add',
        data={'text': 'I love this project!'}
    )
    
    # Verify mood and reflection saved
    with app.app_context():
        db = get_db()
        entry = db.execute('SELECT * FROM entries').fetchone()
        assert entry['mood'] == 'excited'
        assert entry['reflection'] == 'Keep up the enthusiasm!'

@patch('app.entries.call_gemini_api')
def test_gemini_failure_handled_gracefully(mock_gemini, client, auth, app):
    """Test that app handles Gemini API failure."""
    auth.register()
    auth.login()
    
    # Mock Gemini failure (returns fallback values)
    mock_gemini.return_value = {
        'mood': 'neutral',
        'reflection': 'Unable to generate reflection at this time.'
    }
    
    # Add entry should still work
    response = client.post(
        '/entries/add',
        data={'text': 'Test entry'}
    )
    
    # Should redirect successfully
    assert response.headers['Location'] == '/entries/list'
    
    # Entry should be saved with fallback values
    with app.app_context():
        db = get_db()
        entry = db.execute('SELECT * FROM entries').fetchone()
        assert entry is not None
        assert entry['mood'] == 'neutral'