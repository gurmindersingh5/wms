from flask import Blueprint, request, render_template, redirect, url_for, flash

from ...form import SignUpForm
from ...models import User
from ... import db

register_bp = Blueprint('register', __name__, template_folder='templates')


@register_bp.route('/register', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['Username']
        password = request.form['Password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User with username already exists', 'warning')
            return redirect(url_for('register.signup'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login.login'))

    return render_template('register/register.html', form=form)
