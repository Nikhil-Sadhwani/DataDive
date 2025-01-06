from flask import Flask
from flask_login import LoginManager
from config.config import Config
from modules.web_application.models.models import User, db
from flask_migrate import Migrate
from modules.web_application.views.auth import oauth
from modules.web_application.views import register_blueprints
import os

def create_app():
    app = Flask(__name__, template_folder='modules/web_application/templates')
    
    # Use environment variable for configuration, fallback to local config
    app.config.from_object(Config)
    
    # Vercel-specific configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', app.config['SECRET_KEY'])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI'])

    try:
        db.init_app(app)
        print("SQLAlchemy initialized successfully.")
    except Exception as e:
        print(f"Error initializing SQLAlchemy: {e}")
        
    migrate = Migrate(app, db)
    oauth.init_app(app)

    login_manager = LoginManager() 
    login_manager.login_view = "auth.login_google" 
    login_manager.init_app(app)

    @login_manager.user_loader 
    def load_user(user_id): 
        return User.query.get(int(user_id))

    # Custom Jinja2 filter for JavaScript escaping
    def escapejs(text):
        if text is None:
            return ''
        return text.replace('\\', '\\\\') \
                  .replace('\n', '\\n') \
                  .replace('\r', '\\r') \
                  .replace('"', '\\"') \
                  .replace("'", "\\'")

    app.jinja_env.filters['escapejs'] = escapejs

    register_blueprints(app)

    return app

# Vercel requires an app instance
app = create_app()

# For local development
if __name__ == "__main__":
    app.run(debug=True)

# Vercel serverless function entry point
def handler(event, context):
    return app
