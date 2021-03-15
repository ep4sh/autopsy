from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from courses_app import app, flask_bcrypt
from courses_app.model import db, User, Doc
from courses_app.forms import RegistrationForm, LoginForm

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user and flask_bcrypt.check_password_hash(user.user_password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                redirect(url_for('dashboard'))
        else:
            flash(f"Login failed - check the credentials", 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw =  flask_bcrypt.generate_password_hash(form.password.data)\
                                                   .decode('utf-8')
        user = User(user_name=form.username.data, user_password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"An account {form.username.data} has been created", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html')
