from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
from flask_login import login_user, login_required, current_user, logout_user
from urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth

from ...form import LoginForm
from ...models import User, OAuthUser
from ... import db
from ... import oauth

auth0 = oauth.register(
        'auth0',
        client_id='RByXpzargl0vi7A197IYLZWrjiMRD6k1',
        client_secret='inEQsSAOchxYrEObJb0kfQ8X9jn0vg30a_sMYLTb5r5B0CByqGwgImk5yoAawUs3',
        api_base_url=f'https://dev-ide3i4bsx5n6mct1.us.auth0.com',
        access_token_url=f'https://dev-ide3i4bsx5n6mct1.us.auth0.com/oauth/token',
        authorize_url=f'https://dev-ide3i4bsx5n6mct1.us.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
        jwks_uri=f'https://dev-ide3i4bsx5n6mct1.us.auth0.com/.well-known/jwks.json'
    )

login_bp = Blueprint('login', __name__, template_folder='templates')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    form = LoginForm()
    next_page = request.args.get('next')

    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['Username']
        password = request.form['Password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found! Please use correct username or Signup.', 'warning')
            return redirect(url_for('login.login'))
        
        if user.check_password(password=password):
            login_user(user)
            # next parameter is created and inlcuded by login_required decorator in the query string(url) which holds the path to url that user clicked (which the user wanted to access)
            # after its included in the request's url, it is captured in the login view using request.args.get('next')
            # which then passed in the login form while rendering. And on form submit it is caputered again and finally used in redirection.
            session['login_method'] = 'internal_login'
            return redirect(next_page or url_for('home.home'))
        else:
            flash('Wrong credentials', 'danger')
            return redirect(url_for('login.login', next=next_page))

    return render_template('login/login.html', form=form, next=next_page)


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    try:
        username = session.pop('oauth_user')
        user_to_delete = OAuthUser.query.filter_by(username=username).first()
        db.session.delete(user_to_delete)
        db.session.commit()
    except:
        pass
    return redirect(url_for('login.login'))
    # https://{yourDomain}/oidc/logout?id_token_hint={yourIdToken}&post_logout_redirect_uri={yourCallbackUrl}

# Callback endpoint for Auth0
@login_bp.route('/user')
@login_required
def get_user():
    return jsonify({
        'USER': current_user.username,
        })


# Login using Auth0
@login_bp.route('/auth0-login')
def auth0_login():
    '''
    redirects to authorize page at auth0 and after authorization is redirect 
    to callback function with authorization code which can be exchanged for token.
    '''
    return auth0.authorize_redirect(redirect_uri=url_for('login.callback_handling', _external=True))


# Callback for Auth0
@login_bp.route('/callback')
def callback_handling():
    '''
    Control comes here form auth0_login with authorization code.
    Here authorizatoin code is exchagned for token which is again used to fetch user details.
    '''
    # Handles response from Auth0
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    user = OAuthUser.query.filter_by(username=userinfo['nickname']).first()
    if not user:
        try:
            user = OAuthUser(username=userinfo['nickname'])
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return {
                'error': str(e)
            }

    user = OAuthUser.query.filter_by(username=userinfo['nickname']).first()
    if user:
        login_user(user)
        session['oauth_user'] = user.username
        session['login_method'] = 'auth0'
    print(current_user.username)
    return redirect(url_for('profile.load_profile', user=user))