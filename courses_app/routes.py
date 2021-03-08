from flask import render_template, request
from courses_app import app

@app.route('/')
def dashboard():
    return render_template('user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    pass


def show_the_login_form():
    pass
