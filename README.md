#  Autopsy: web app for postmortems

![Autopsy](https://github.com/ep4sh/autopsy/actions/workflows/main.yml/badge.svg)


![Autopsy](https://user-images.githubusercontent.com/19505042/113065705-f7f9f000-91c1-11eb-92be-1821648954b0.jpg) Autopsy is free, Flask-based Postmortem web app.


Autopsy spreads postmortems culture, involves people to learn on the failures.

## Concepts

* Users can add, update postmortems
* You can update only your postmortem
* User with id == 1 is a service's admininstrator

## Screenshots

#### Register
![register](https://user-images.githubusercontent.com/19505042/113065724-faf4e080-91c1-11eb-8940-87973a30a484.gif)
#### Login
![login](https://user-images.githubusercontent.com/19505042/113065716-f9c3b380-91c1-11eb-9e99-cdb9070487e5.gif)
#### Reset Password
![forgot_password](https://user-images.githubusercontent.com/19505042/113065710-f92b1d00-91c1-11eb-803f-c11ff2a538b4.gif)
#### Dashboard
![dashboard](https://user-images.githubusercontent.com/19505042/113065708-f8928680-91c1-11eb-95b4-e04170d1a947.gif)
#### Postmortems
![list_postmortems](https://user-images.githubusercontent.com/19505042/113065713-f9c3b380-91c1-11eb-9e30-dc7117d90edb.gif)
#### View a postmortem
![current_postmortem](https://user-images.githubusercontent.com/19505042/113065706-f8928680-91c1-11eb-8735-1fb9a1a89c24.gif)
#### New postmortem
![new_postmortem](https://user-images.githubusercontent.com/19505042/113065720-fa5c4a00-91c1-11eb-8fe0-d7eaab7b93ee.gif)
#### Update postmortem
![update_postmortem](https://user-images.githubusercontent.com/19505042/113065729-fb8d7700-91c1-11eb-8c55-d4238c5dfa80.gif)
#### Search in postmortems
![search](https://user-images.githubusercontent.com/19505042/113065726-faf4e080-91c1-11eb-8a3c-f246aa974bf2.gif)
#### Update profile
![profile](https://user-images.githubusercontent.com/19505042/113065721-fa5c4a00-91c1-11eb-82e2-741e2914845e.gif)
#### Admin page
![admin](https://user-images.githubusercontent.com/19505042/113065702-f7615980-91c1-11eb-8715-467e39e847fb.gif)
#### Create a support ticket
![support](https://user-images.githubusercontent.com/19505042/113065728-fb8d7700-91c1-11eb-82ac-652288c5790d.gif)

## Features

* Dashboard shows latest and random postmortems
* Postmortems provides lists postmortems with CRU(D) capabilities
* Search performs search operation in Postmortems' names
* Admin manages all the service's data in Flask-admin way
* Users can register, login, update the profile, create support tickets (attaching screenshot), logout and restore their password via email.

## Roadmap
[Trello](https://trello.com/b/ngqvbNgt/autopsy)

## Requirements

* python3
* PostgreSQL
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
python3 -m venv path/to/new/virtual/environment
source path/to/new/virtual/environment
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
|MAIL_SERVER| smtp.example.com | Yes | SMTP server URL|
|MAIL_PORT| 465 | Yes | SMTP server port|
|MAIL_USE_SSL| True | depends | SMTP server SSL|
|MAIL_USERNAME| <noreply@example.com> | Yes | Username for no-reply@ account|
|MAIL_PASSWORD| <account_password>| Yes | Password for no-reply account|
|DATABASE_HOST| <database_host> | Yes | Database host|
|DATABASE_USER| docker | Yes | Database Username|
|DATABASE_PASSWORD| docker | Yes | Database Password|
|DATABASE_PORT| 5432 | depends | Database Port|
|DATABASE_NAME| docker | Yes | Database Name|
|SQLALCHEMY_TRACK_MODIFICATIONS| True | No | Track DB modification|

#### Install dependencies
```
pip3 install -r requirements.txt
```

#### Apply DB migrations
```
flask db migrate
flas db upgrade
```

#### Run app
```
uswgi app.ini
```

#### Go to
```
http://localhost:5000/
```


## PostgreSQL development instance
There is a way to spin-up development PostgreSQL database in container via docker-compose.
```
cd docker_misc/db
docker-compose up -d
```

Database credentials can be found in `docker_misc/db/docker-compose.yml`:
```
- APP_DB_USER=docker
- APP_DB_PASS=docker
- APP_DB_NAME=docker
```

:hankey: Be aware from running the production database instance this way and from other monsters!


## Creating a Docker container


### Create a builder (:hugs: The image can be built without buildkit)
```
docker buildx create --name mbuilder --platform linux/arm64,linux/arm/v8,linux/armv7,linux/amd64  --use
```

### Exporting ENV vars

```
export $(cat .env)
```

### x64 - Build docker image
```
APP_VERSION=$(git describe)
docker buildx build --platform=linux/amd64 -t ep4sh/autopsy:$APP_VERSION \
  --build-arg FLASK_APP=$FLASK_APP \
  --build-arg FLASK_ENV=$FLASK_ENV \
  --push .
```

### x64 - Run docker container
```
docker run -d -v $PWD/.env:/app/.env -v $PWD/app.ini:/app/app.ini \
  -p5000:5000 ep4sh/autopsy:$APP_VERSION
```


## Icon authors:
[DinosoftLabs](https://www.flaticon.com/authors/dinosoftlabs)


[FreePik](https://www.freepik.com/)

## Books
I'm in love with books. If you want to thank me, just help me to buy books from the list

[![buy-me-a-book](https://img.shields.io/badge/Amazon-Buy%20me%20a%20book-important)](https://www.amazon.com/hz/wishlist/ls/3NSSXQK5CTS8N?ref_=wl_share)
