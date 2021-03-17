from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from autopsy_app import app, flask_bcrypt
from autopsy_app.model import db, User, Doc
from autopsy_app.forms import RegistrationForm, LoginForm, ProfileForm

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(user_email=form.email.data).first()
            if user and flask_bcrypt.check_password_hash(user.user_password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                redirect(url_for('dashboard'))
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
        hashed_pw = flask_bcrypt.generate_password_hash(form.password.data)\
                                                        .decode('utf-8')
        user = User(user_email=form.email.data, user_password=hashed_pw,
                    user_name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash(f"An account {form.email.data} has been created", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        hashed_pw = flask_bcrypt.generate_password_hash(form.password.data)\
                                                        .decode('utf-8')
        current_user.user_name = form.name.data
        current_user.password = hashed_pw
        db.session.commit()
        flash(f"An account has been updated", 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@app.route('/postmortems')
@login_required
def postmortem():
    pass

@app.route('/notifications')
@login_required
def notify():
    pass
