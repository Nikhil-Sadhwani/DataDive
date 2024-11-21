from flask import Blueprint, session, redirect, url_for, flash
from authlib.integrations.flask_client import OAuth
from flask_login import login_user, logout_user
from modules.web_application.models.models import db, User

import os

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()


google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)

@auth_bp.route('/login/google')
def login_google():
    try:
        redirect_uri = url_for('auth.authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        return "Error occurred during login", 500

@auth_bp.route("/authorize/google")
def authorize_google():
    token = google.authorize_access_token()
    userinfo_endpoint = google.server_metadata['userinfo_endpoint']
    res = google.get(userinfo_endpoint)
    user_info = res.json()

    name = user_info['name']
    email = user_info['email']
    picture = user_info['picture']

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            name=name,
            email=email,
            social_login_provider='google',
            profile_picture=picture
        )
        db.session.add(user)
        db.session.commit()

    session['email'] = email
    session['outh_token'] = token

    login_user(user)
    flash("You have been logged in!", "success")
    return redirect(url_for('dashboard.dashboard'))

@auth_bp.route("/logout")
def logout():
    session.clear()
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for('main.index'))
