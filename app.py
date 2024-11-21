from flask import Flask
from flask_login import LoginManager
from config.config import Config
from modules.web_application.models.models import User, db
from flask_migrate import Migrate
from modules.web_application.views.auth import oauth
from modules.web_application.views import register_blueprints

def create_app():

    app = Flask(__name__, template_folder='modules/web_application/templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    oauth.init_app(app)

    login_manager = LoginManager() 
    login_manager.login_view = "auth.login_google" 
    login_manager.init_app(app)

    @login_manager.user_loader 
    def load_user(user_id): 
        return User.query.get(int(user_id))

    register_blueprints(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
