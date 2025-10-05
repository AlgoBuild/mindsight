import os
from flask import Flask

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'mindsight.db'),
    )
    
    if test_config is None:
        # Load the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register database functions
    from . import db
    db.init_app(app)
    
    # Register authentication blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    
    # Register entries blueprint
    from . import entries
    app.register_blueprint(entries.bp)
    
    # Simple home route
    @app.route('/')
    def index():
        return 'Mindsight - Smart Journal'
    
    return app