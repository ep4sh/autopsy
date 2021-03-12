from flask import render_template, request, flash, redirect, url_for
from courses_app import app
from courses_app.forms import RegistrationForm, LoginForm

@app.route('/')
def dashboard():
    return render_template('user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('dashboard'))
        else:
            flash(f"Login failed - check the credentials", 'danger')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"An account {form.email.data} has been created", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

