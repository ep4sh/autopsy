"""
Add Flask routes for Autopsy Web App

Methods:
    def dashboard() -> render_template
    def reset() -> render_template / redirect
    def reset_password(token) -> render_template / redirect
    def login() -> render_template / redirect
    def register()   -> render_template / redirect
    def logout() -> redirect
    def profile() -> render_template
    def postmortems() -> render_template
    def add_postmortem() -> render_template / redirect
    def get_postmortem(url) -> render_template
    def update_postmortem(url) -> render_template / redirect
    def search() -> render_template / redirect
    def support() -> render_template / redirect
    def page_not_found(e) -> render_template
    def page_forbidden(e) -> render_template
"""
import datetime
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from autopsy_app import app
from autopsy_app.admin import adm
from autopsy_app.model import db, User, Role, Mortem, Support
from autopsy_app.forms import (RegistrationForm, LoginForm, ProfileForm,
                               PostmortemForm, SupportForm, RequestResetForm,
                               ResetForm)
from autopsy_app.mail import send_email, send_admin_email
from autopsy_app.funcs import (define_mortem_url, choose_random_mortem,
                               auto_tag, generate_password,
                               verify_password, get_tags, resize_screenshot)


@app.route('/')
@login_required
def dashboard():
    """
    Show a Autopsy dashboard with Recently added and Random Postmortems
    """
    # Getting recent postmortems
    recent_mortems = Mortem.query.order_by(Mortem.mortem_created.desc()).\
                    limit(3).all()
    # Getting random postmortem
    max_mortem = Mortem.query.order_by(Mortem.id.desc()).limit(1).first()
    if max_mortem is not None:
        max_mortem_id = max_mortem.id
        rnd_mortem_id = choose_random_mortem(max_mortem_id)
        rnd_mortem = Mortem.query.get(rnd_mortem_id)
    else:
        rnd_mortem = None
    return render_template('dashboard.html', mortems=recent_mortems,
                           rnd_mortem=rnd_mortem)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    """
    Show a RequestResetForm to reset user's password via email
    """
    if current_user.is_authenticated:
        return redirect("/")
    form = RequestResetForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(user_email=form.email.data).first()
            if user:
                token = user.generate_token()
                send_email(user.user_email, token)
                flash('Reset URL has been sent to your email',
                      'info')
            else:
                flash('Reset failed - check the login', 'danger')
            return redirect(url_for('login'))
    now = datetime.datetime.utcnow()
    return render_template('reset.html', form=form, now=now)


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Check reset token and show ResetForm to reset a password
    """
    if current_user.is_authenticated:
        return redirect("/")
    user = User.verify_token(token)
    if user is None:
        flash('A token has been expired', 'warning')
        return redirect(url_for('reset'))
    form = ResetForm()
    if request.method == "POST" and user:
        if form.validate_on_submit():
            user.user_password = generate_password(form.password.data)
            db.session.commit()
            flash(f'An password for {user.user_email} has been reset',
                  'success')
            return redirect(url_for('login'))
    now = datetime.datetime.utcnow()
    return render_template('reset_pass.html', form=form, now=now)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticate the user
    """
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(user_email=form.email.data).first()
            if user and verify_password(user.user_password,
                                        form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    flash('Login failed - check the credentials', 'danger')
                    return redirect(url_for('dashboard'))
    now = datetime.datetime.utcnow()
    return render_template('login.html', form=form, now=now)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register new user
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # check if root user exists and assign a role
        role = "user" if User.query.first() else "admin"
        hashed_pw = generate_password(form.password.data)
        user = User(user_email=form.email.data,
                    user_password=hashed_pw,
                    user_name=form.name.data)
        roles = Role.query.filter_by(name=role).first()
        user.roles = [roles]
        db.session.add(user)
        db.session.commit()
        flash(f"An account {form.email.data} has been created", 'success')
        return redirect(url_for('login'))
    now = datetime.datetime.utcnow()
    return render_template('register.html', form=form, now=now)


@app.route('/logout')
def logout():
    """
    Logout current user
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Show profile page to change name, password, avatar
    """
    form = ProfileForm()
    if form.validate_on_submit():
        hashed_pw = generate_password(form.password.data)
        current_user.user_name = form.name.data
        current_user.password = hashed_pw
        if form.avatar.data != "":
            current_user.user_image = form.avatar.data
        db.session.commit()
        flash('An account has been updated', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)


@app.route('/postmortems')
@login_required
def postmortems():
    """
    Show postmortems list
    """
    MORTEMS_PER_PAGE = 7
    page = request.args.get('page', type=int, default=1)
    mortems = Mortem.query.order_by(
              Mortem.id.desc()).paginate(page=page,
                                         per_page=MORTEMS_PER_PAGE,
                                         error_out=False)
    return render_template('postmortems.html', mortems=mortems)


@app.route('/postmortems/add', methods=['GET', 'POST'])
@login_required
def add_postmortem():
    """
    Add new postmortem
    """
    form = PostmortemForm()
    if form.validate_on_submit():
        title = form.title.data
        impact = form.impact.data
        content = form.mortem.data
        resolution = form.resolution.data
        url = define_mortem_url()
        now = datetime.datetime.utcnow()
        uid = current_user.id
        tags = auto_tag(form.mortem.data)
        mortem = Mortem(mortem_name=title, mortem_content=content,
                        mortem_url=url, mortem_created=now,
                        mortem_resolution=resolution, mortem_tags=tags,
                        mortem_impact=impact, mortem_updated=now, user_id=uid)
        db.session.add(mortem)
        db.session.commit()
        flash('The mortem has been added', 'success')
        return redirect(url_for('add_postmortem'))
    return render_template('add_postmortem.html', form=form)


@app.route('/postmortems/<url>')
@login_required
def get_postmortem(url):
    """
    Show paricular postmortem details
    """
    mortem = Mortem.query.filter_by(mortem_url=url).first()
    mortem.mortem_tags = get_tags(mortem.mortem_tags)
    return render_template('get_postmortem.html', mortem=mortem)


@app.route('/postmortems/<url>/update', methods=['GET', 'POST'])
@login_required
def update_postmortem(url):
    """
    Update paricular postmortem details
    """
    mortem = Mortem.query.filter_by(mortem_url=url).first()
    if mortem.author != current_user:
        abort(403)
    form = PostmortemForm()
    # passing value of Mortem content to the textarea
    if form.validate_on_submit():
        mortem.mortem_name = form.title.data
        mortem.mortem_impact = form.impact.data
        mortem.mortem_content = form.mortem.data
        mortem.mortem_resolution = form.resolution.data
        mortem.mortem_updated = datetime.datetime.utcnow()
        mortem.mortem_tags = auto_tag(form.mortem.data)
        db.session.commit()
        flash('The mortem has been updated', 'success')
        return redirect(url_for('get_postmortem', url=url))
    elif request.method == "GET":
        form.title.data = mortem.mortem_name
        form.impact.data = mortem.mortem_impact
        form.mortem.data = mortem.mortem_content
    return render_template('update_postmortem.html', mortem=mortem, form=form)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    Perform search per Postmortems
    """
    def _get_results(q):
        MORTEMS_PER_PAGE = 3
        page = request.args.get('page', type=int, default=1)
        mortems = Mortem.query.filter(
                  Mortem.mortem_name.like(f"%{q}%")).paginate(
                  page=page, per_page=MORTEMS_PER_PAGE, error_out=False)
        return page, mortems
    if request.method == 'POST':
        query = request.form['search_query']
        page, mortems = _get_results(query)
        if page != 1:
            return redirect(url_for('search', query=query, page=1))
    elif request.method == 'GET':
        query = request.args.get('query', type=str, default=None)
        if query is not None:
            query = query.strip("'")
            page, mortems = _get_results(query)
        else:
            mortems = None
    return render_template('search.html', mortems=mortems, query=query)


@app.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    """
    Create a support case (bug,error,issue)
    """
    form = SupportForm()
    if form.validate_on_submit():
        subject = form.subject.data
        content = form.content.data
        attach = form.attach.data
        if attach:
            attach_data = resize_screenshot(attach.stream)
        else:
            attach_data = b''
        now = datetime.datetime.utcnow()
        uid = current_user.id
        support_case = Support(support_subject=subject,
                               support_content=content,
                               support_created=now,
                               support_attach=attach_data,
                               user_id=uid)
        send_admin_email(db, support_case)
        db.session.add(support_case)
        db.session.commit()
        flash('The Support Case has been created', 'warning')
        return redirect(url_for('support'))
    return render_template('support.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    """
    HTTP 404 Handler
    """
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    """
    HTTP 403 Handler
    """
    return render_template('403.html'), 403
