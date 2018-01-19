# [Elite Dangerous Events](http://elitedangerousevents.us-east-1.elasticbeanstalk.com/) 1.0.0

A site for commanders in the Elite Dangerous galaxy to create and join in player created events. 

## Getting Started

### Prerequisites

```
Python 3
Pip 
Virtualenv
```

### Installing

Setup virtual environment with python 3 flagged

```
virtualenv -p python3 eliteEvents
```

Change directory into virtual environment and activate

```
cd eliteEvents/ && source bin/activate
```

Clone repo into virtual environment

```
git clone https://github.com/CCecilia/eliteDangerousEvents.git
```

Change to root project directory

```
cd eliteDangerousEvents/eliteEvents/
```

Install dependencies from requirements.txt

```
pip install -r requirements.txt
```

Database

```
The project is setup for MySql but the the default Sqlite3 database code is just commented out
so if you want to use the slqlite DB just comment out the MySql code. But if you use a 
MySql database be sure to add the credentials to secret.py as explained in the next step. Sqlite3 
is advised for development.
```

Create secret.py file in eliteDangerousEvents/eliteEvents/eliteEvents/

```
NOTE
secret.py should contain the django SECRET KEY and Google Oauth key as below. As well 
as the database information if you decide to to use a mysql database. 
If no secret.py is created a random secret key is generated and Oauth is unusable.
python manage.py runserver
```

secret.py

```
google_oauth_key = GOOGLE API SECRET
google_oauth_secret = GOOGLE API ID
django_secret_key = YOUR DJANGO SECRET KEY
facebook_oauth_key = FB App ID
facebook_oauth_secret = FB App Secret key
database_name = SCHEMA NAME
database_username = USERNAME
database_password = PASSWORD
database_endpoint = DATABASE URL
```

Start your local server

```
python manage.py runserver
```

Upon success you will see 
```
System check identified no issues (0 silenced).
December 13, 2017 - 20:11:10
Django version 2.0, using settings 'eliteEvents.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Copy and paste http://localhost:8000/ into your browser.

## Running the tests

```
python manage.py test
```

## Optional
* Auto fill location information
* download [populated_systems.json](https://eddb.io/archive/v5/systems_populated.json)

```
For auto-filling of populated systems download file and save to website/media/uploads. 
Then call Utility.parsePopulatedSystems() in website/views.py to parse the data in the file.
```
* Crontab commands
* [additional info](https://github.com/kraiz/django-crontab)
```
python manage.py crontab add - add the hourly and daily cleaning of expired events/lfg post jobs
python manage.py crontab show - show active jobs
python manage.py crontab remove - remove active jobs

```

## Built With

* [Python3.6.3](https://www.python.org/downloads/release/python-363/)
* [PIP](https://pypi.python.org/pypi/pip)
* [Django](https://www.djangoproject.com/)
* [Bootstrap](http://getbootstrap.com/)
* other dependecies in requirements.txt

## Versioning

[SemVer](http://semver.org/) for versioning. 

## Authors

* **Christian Cecilia** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Frontier Developments](https://www.frontier.co.uk/) for making an awesome space sim [Elite Dangerous](https://www.elitedangerous.com/)
* CMDR (SpyTec)[https://github.com/SpyTec] for [edassets.org](https://github.com/SpyTec/EDAssets) [Git repo](https://github.com/SpyTec/EDAssets)
