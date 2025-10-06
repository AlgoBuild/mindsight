import sqlite3
import pytest
from app.db import get_db

def test_get_db(app):
    """Test that get_db returns same connection within context."""
    with app.app_context():
        db = get_db()
        assert db is get_db()

def test_close_db(app):
    """Test that database is closed after context."""
    with app.app_context():
        db = get_db()
    
    # After context, connection should be closed
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    """Test the init-db CLI command."""
    class Recorder:
        called = False
    
    def fake_init_db():
        Recorder.called = True
    
    monkeypatch.setattr('app.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called