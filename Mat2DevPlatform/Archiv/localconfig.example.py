import os

from django_cron import Schedule

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's9735p91f*62q1pe%o$_l1u10-pi6wgh_gxjy3#!+(=x*^u_i5'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# dont use in production. has no effect if DEBUG = False
LOG_QUERIES = True

MEDIA_ROOT="data"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {

    # USE ONLY FOR DEVELOPMENT
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    },

    # USE POSTGRES FOR PRODUCTION
    #    'default': {
    #        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #        'NAME': 'scrambl_production',
    #        'USER': 'scrambl_production',
    #        'PASSWORD': '<password>',
    #        'HOST': 'localhost',
    #        'PORT': '5432',
    #    }

    #'x28_ontology': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'ontology',
    #    'USER': 'user',
    #    'PASSWORD': 'password',
    #    'HOST': '127.0.0.1',
    #    'PORT': '3306',
    #}

}

FRONTEND_BASE = "http://localhost:3000/"
BACKEND_BASE = "http://localhost:8000/"

# where the data-folder is served
MEDIA_URL="http://localhost:8000/static/"

EMAIL_HOST = "some.host"
EMAIL_PORT = 465
EMAIL_HOST_USER = "some-user"
EMAIL_HOST_PASSWORD = "1234"
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "Scrambl <scrambl@scrambl.org>"

ATTACHMENT_MAX_SIZE = 20 # MB

# comment this if DEBUG = True
# only allow localhost (proxy)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

BEXIO_CLIENT_ID = 'some-id'
BEXIO_CLIENT_SECRET = 'some-secret'
BEXIO_ISSUER = 'https://idp.bexio.com/'
BEXIO_API_BASE = 'https://api.bexio.com/'
BEXIO_UI_BASE = 'https://office.bexio.com/index.php/'
BEXIO_USER_ID = 1
BEXIO_ACCOUNT_ID = 343 # 3401 Bruttoerlöse Kreditgeschäft
BEXIO_CRON_EVERY_MINS = 5


# Warning: set to True in production
# django is async and views serving static files slow it down a lot
STATIC_FILES_VIA_NGINX = False
STATIC_FILES_NGINX_PATH = '/static/data/'

# Internal notification such as new company, new offer
INTERNAL_NOTIFICATION_EMAIL = "some-address@scrmabl.org"

LINKEDIN_OAUTH2_CALLBACK_URL = "https://<scrambl-frontend>/login/linkedin/callback/"

# monitoring
SENTRY_ENABLED = False
SENTRY_DSN = "<dsn>"
SENTRY_TRACES_SAMPLE_RATE = 1.0
SENTRY_DEFAULT_PII = True

#x28 JSON API URL
X28_ENABLE_POLLING = False
X28_URL = "https://api.x28.ch/export/api/jobs/json"
X28_URL_MODIFIED = "https://api.x28.ch/export/api/jobs/updates/json"
X28_USER = "<user>"
X28_PASS = "<pass>"

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#        'LOCATION': 'unique-scrambl',
#    }
#}

# admin email addresses (error notifications
ADMINS = [
    ("Max Mustermann", 'mustermann@example.com')
]

# defines when flexworkers are notified about new tenders
NOTIFY_ABOUT_NEW_TENDERS_SCHEDULE = Schedule(run_at_times=['12:00']) # dailay at 12:00
#NOTIFY_ABOUT_NEW_TENDERS_SCHEDULE = Schedule(run_every_mins=3)

NEOMODEL_NEO4J_BOLT_URL = 'bolt://neo4j:password@localhost:7687'

LIMIT_MAIL_TO_DEV = False

SHORT_URL_BASE = 'http://localhost:8000/s/'