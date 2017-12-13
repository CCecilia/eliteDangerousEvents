# Elite Dangerous Events

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

'''
virtualenv -p python3 eliteEvents
''' 

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

Start your local server

```
python manage.py runserver
```

Upon success you will see 
'''
System check identified no issues (0 silenced).
December 13, 2017 - 20:11:10
Django version 2.0, using settings 'eliteEvents.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
'''
Copy and paste http://127.0.0.1:8000/ into your browser.

## Running the tests

```
python manage.py test
```

## Built With

* [Python3.6.3]
* [Django](https://www.djangoproject.com/)
* [PIP](https://pypi.python.org/pypi/pip)

## Versioning

[SemVer](http://semver.org/) for versioning. 

## Authors

* **Christian Cecilia** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Frontier Developments for making an awesome space sim
* CMDR SpyTec for creating (http://edassets.org/)
