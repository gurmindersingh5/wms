from flask import Flask, redirect, url_for, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from flask_login import LoginManager, login_user, current_user


# Configure blueprints
google_bp = make_google_blueprint(
    client_id='',
    client_secret='',
    scope=["profile", "email"] 
)


@google_bp.route('/login/google')
def login_google():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    # Here you'd create/login a user based on 'resp' and then:
    flash("You have successfully logged in with Google")
    return redirect(url_for('home.home')) 
