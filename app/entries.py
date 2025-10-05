from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('entries', __name__, url_prefix='/entries')

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    """Add a new journal entry."""
    if request.method == 'POST':
        text = request.form['text']
        error = None

        if not text:
            error = 'Journal entry text is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO entries (user_id, text) VALUES (?, ?)',
                (g.user['id'], text)
            )
            db.commit()
            flash('Entry saved successfully!')
            return redirect(url_for('entries.list'))

    return render_template('entries/add_entry.html')

@bp.route('/list')
@login_required
def list():
    """Display all journal entries for the logged-in user."""
    db = get_db()
    entries = db.execute(
        'SELECT id, text, mood, reflection, timestamp'
        ' FROM entries'
        ' WHERE user_id = ?'
        ' ORDER BY timestamp DESC',
        (g.user['id'],)
    ).fetchall()
    
    return render_template('entries/list.html', entries=entries)