from modules.web_application.views.auth import auth_bp
from modules.web_application.views.main import main_bp
from modules.web_application.views.prompt import prompt_bp
from modules.web_application.views.dashboard import dashboard_bp
from modules.web_application.views.scrape import scrape_bp

# List of all blueprints to be registered
blueprints = [
    auth_bp,
    main_bp,
    prompt_bp,
    dashboard_bp,
    scrape_bp,
]

# Function to register all blueprints to the app
def register_blueprints(app):
    for bp in blueprints:
        app.register_blueprint(bp)
