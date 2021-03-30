#  Autopsy: web app for postmortems

![Autopsy](autopsy_app/static/autopsy.svg) Autopsy is free, Flask-based Postmortem web app. Autopsy spreads postmortems culture, involves people to learn on the failures.

## Concepts

* Users can add, update postmortems
* You can update only your postmortem
* User with id == 0 is a service's admininstrator

## Features

* Dashboard shows latest and random postmortems
* Postmortems shows list of postmortems with CRUD
* Search performs search operation in Postmortems' names
* Admin page manages all the service's data in Flask-admin way
* Users can register, login, update the profile, create support tickets (attaching screenshot), logout and restore their password via email.

## Roadmap
[Trello](https://trello.com/b/ngqvbNgt/autopsy)

## Requirements

* python3
* SMTP server (for password reset)

## Installation

#### Clone the project
```
git clone https://github.com/ep4sh/autopsy.git
cd autopsy
```

#### Python venv
I'd recommend to use python [virtual environment](https://docs.python.org/3/library/venv.html) to install all dependencies:
```
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment
```

#### Dotenv files
Autopsy reads the key-value pairs from `.env` files and adds them to environment variable
```
cp .env.example .env
```

#### Dotenv file settings description

|Variable | Value(default)  | Required for update |Description|
--- | --- | --- |---
|FLASK_APP| main.py| No |Name of the main module|
|FLASK_ENV|development| depends |[Flask mode](https://flask.palletsprojects.com/en/1.1.x/config/?highlight=debug#DEBUG)|
|FLASK_SECRET| abcdef | Yes| [Flask Secret](https://flask.palletsprojects.com/en/1.1.x/config/?highlight=secret#SECRET_KEY)|
|MAIL_SERVER| smtp.yandex.ru | Yes | SMTP server URL|
|MAIL_PORT| 465 | Yes | SMTP server port|
|MAIL_USE_SSL| True | depends | SMTP server SSL|
|MAIL_USERNAME| login | Yes | Username for no-reply@ account|
|MAIL_PASSWORD| password | Yes | Password for no-reply account|
|SQLALCHEMY_DATABASE_URI| "sqlite:///autopsy.db"| Yes | Database URI|
|SQLALCHEMY_TRACK_MODIFICATIONS| main.py| depends| Track DB modification|

## Icon authors:
[DinosoftLabs](https://www.flaticon.com/authors/dinosoftlabs)
[FreePik](https://www.freepik.com/)

## Books
I'm in love with books. If you want to thank me, just help me to buy books from the list

[![buy-me-a-book](https://img.shields.io/badge/Amazon-Buy%20me%20a%20book-important)](https://www.amazon.com/hz/wishlist/ls/3NSSXQK5CTS8N?ref_=wl_share)
