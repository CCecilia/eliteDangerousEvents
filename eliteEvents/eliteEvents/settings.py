# import djcelery
import os
import random
import string
from .secret import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# gen random secret key
random_key = ''.join([random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(50)])

DEBUG = True

if django_secret_key:
    SECRET_KEY = django_secret_key
else:
    SECRET_KEY = random_key

if google_oauth_key and google_oauth_secret:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = google_oauth_key
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = google_oauth_secret
else:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

if facebook_oauth_key and facebook_oauth_secret:
    SOCIAL_AUTH_FACEBOOK_KEY = facebook_oauth_key
    SOCIAL_AUTH_FACEBOOK_SECRET = facebook_oauth_secret
else:
    SOCIAL_AUTH_FACEBOOK_KEY = ''
    SOCIAL_AUTH_FACEBOOK_SECRET = ''

ALLOWED_HOSTS = [
    'localhost',
    'elitedangerousevents.us-east-1.elasticbeanstalk.com',
    'www.elitedangerousevents.com'
]


INSTALLED_APPS = [
    'website.apps.WebsiteConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_crontab',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eliteEvents.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'eliteEvents.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': database_name, 
        'USER': database_username,
        'PASSWORD': database_password,
        'HOST': database_endpoint,
        'PORT': '3306',
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'social_core.backends.facebook.FacebookOAuth2',  # for Facebook authentication
)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'website/static/')

LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/'


CRONJOBS = [
    ('0 */1 * * *', 'eliteEvents.cron.hourlyClean'),
    ('59 23 */1 * 0-6', 'eliteEvents.cron.dailyClean')
]
