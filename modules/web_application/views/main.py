from flask import Blueprint, render_template
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template("index.html", authenticated=True)
    return render_template("index.html", authenticated=False)
