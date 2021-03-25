import datetime
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from autopsy_app import app, flask_bcrypt
from autopsy_app.model import db, User, Mortem, Support
from autopsy_app.forms import RegistrationForm, LoginForm, ProfileForm
from autopsy_app.forms import PostmortemForm, SupportForm
from autopsy_app.funcs import define_mortem_url, choose_random_mortem


@app.route('/')
@login_required
def dashboard():
    # Getting recent postmortems
    recent_mortems = Mortem.query.order_by(Mortem.mortem_created.desc()).\
                    limit(3).all()
    # Getting random postmortem
    max_mortem_id = Mortem.query.order_by(Mortem.id.desc()).limit(1).first().id
    rnd_mortem_id = choose_random_mortem(max_mortem_id)
    rnd_mortem = Mortem.query.get(rnd_mortem_id)
    return render_template('dashboard.html', mortems=recent_mortems,
                           rnd_mortem=rnd_mortem)


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


@app.route('/postmortems/<url>/update', methods=['GET', 'POST'])
@login_required
def update_postmortem(url):
    mortem = Mortem.query.filter_by(mortem_url=url).first()
    if mortem.author != current_user:
        abort(403)
    form = PostmortemForm()
    # passing value of Mortem content to the textarea
    if form.validate_on_submit():
        mortem.mortem_name = form.title.data
        mortem.mortem_content = form.mortem.data
        mortem.mortem_updated = datetime.datetime.utcnow()
        db.session.commit()
        flash('The mortem has been updated', 'success')
        return redirect(url_for('get_postmortem', url=url))
    elif request.method == "GET":
        form.title.data = mortem.mortem_name
        form.mortem.data = mortem.mortem_content
    return render_template('update_postmortem.html', mortem=mortem, form=form)


@app.route('/notifications')
@login_required
def notify():
    pass


@app.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    form = SupportForm()
    if form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        attach = form.attach.data
        if attach:
            attach_data = attach.read()
        else:
            attach_data = b''
        now = datetime.datetime.utcnow()
        uid = current_user.id
        support_case = Support(support_subject=subject,
                               support_content=content,
                               support_created=now, support_attach=attach_data,
                               user_id=uid)
        db.session.add(support_case)
        db.session.commit()
        flash('The Support Case has been created', 'warning')
        return redirect(url_for('support'))
    return render_template('support.html', form=form)
