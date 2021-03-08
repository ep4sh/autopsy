from flask import render_template, request
from courses_app import app
from courses_app.forms import RegistrationForm, LoginForm

@app.route('/')
def dashboard():
    return render_template('user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login()

def do_the_login():
    pass

def show_the_login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return do_the_reg()
    else:
        return show_the_reg()

def do_the_reg():
    pass

def show_the_reg():
    form = RegistrationForm()
    return render_template('register.html', form=form)
