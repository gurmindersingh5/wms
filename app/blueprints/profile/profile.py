from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
# from ...models import User, OAuthUser

profile_bp = Blueprint('profile', __name__, template_folder='templates')


@profile_bp.route('/me')
# @login_required
def load_profile():
    user = "Not found"
    try:
        user = current_user.username
    except:
        user = 'You are Logged in but something went wrong while retreiving user information.'
    return render_template('profile/profile.html', user=user)