import datetime
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from autopsy_app import app, flask_bcrypt
from autopsy_app.model import db, User, Mortem
from autopsy_app.forms import RegistrationForm, LoginForm, ProfileForm
from autopsy_app.forms import PostmortemForm
from autopsy_app.funcs import define_mortem_url


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
            if user and flask_bcrypt.check_password_hash(user.user_password,
                                                         form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                redirect(url_for('dashboard'))
                if next_page:
                    return redirect(next_page)
                else:
                    redirect(url_for('dashboard'))
            else:
                flash('Login failed - check the credentials', 'danger')
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
        if form.avatar.data != "":
            current_user.user_image = form.avatar.data
        else:
            current_user.user_image
        db.session.commit()
        flash('An account has been updated', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)


@app.route('/postmortems')
@login_required
def postmortems():
    mortems = Mortem.query.all()
    return render_template('postmortems.html', mortems=mortems)


@app.route('/postmortems/add', methods=['GET', 'POST'])
@login_required
def add_postmortem():
    form = PostmortemForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.mortem.data
        url = define_mortem_url()
        now = datetime.datetime.utcnow()
        uid = current_user.id
        mortem = Mortem(mortem_name=title, mortem_content=content,
                        mortem_url=url, mortem_created=now,
                        mortem_updated=now, user_id=uid)
        db.session.add(mortem)
        db.session.commit()
        flash('The mortem has been added', 'success')
        return redirect(url_for('add_postmortem'))
    return render_template('add_postmortem.html', form=form)


@app.route('/postmortems/<url>')
@login_required
def get_postmortem(url):
    mortem = Mortem.query.filter_by(mortem_url=url).first()
    return render_template('get_postmortem.html', mortem=mortem)


@app.route('/notifications')
@login_required
def notify():
    pass
