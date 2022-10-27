"""

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import sentry_sdk
from corsheaders.defaults import default_headers
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
import os

from scrambl.localconfig import *

# Application definition

INSTALLED_APPS = [
    'csvexport',
    'channels',
    'django_extensions',
    'related_admin',
    'admin_interface',
    'colorfield',
    'dal',
    'dal_select2',
    'django_admin_multiple_choice_list_filter',
    'nested_admin',
    'django_summernote',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'sortedm2m',
    'users.apps.UsersConfig',
    'corsheaders',
    'djmoney',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'rest_auth',
    'rest_auth.registration',
    'django_cron',
    'django_neomodel',
    'core',
    'mailer',
    'shortener',
    'mail',
    'esco',
    'chat',
    'attachments',
    'billing',
    'customers',
    'contractor',
    'profiles',
    'projects',
    'x28',
    'x28_ontology',
    'skills',
    'stories',
    'bexio',
    'guardian',
    'django_cleanup.apps.CleanupConfig', # automatically deletes attachment files on model delete
    "django.contrib.postgres" # postgres-specific functions
]

SITE_ID = 1

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DJANGO_CRON_LOCK_BACKEND = "django_cron.backends.lock.database.DatabaseLock"
DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 14  # days
FAILED_RUNS_CRONJOB_EMAIL_PREFIX = "[cron]: "

CRON_CLASSES = [
    "chat.cron.NotificationCronJob",
    "bexio.cron.BexioCronJob",
    "attachments.cron.AttachmentCronJob",
    'contractor.cron.DetailsChangeNotificationCronJob',
    'projects.cron.ProjectsCronJob',
    'x28.cron.FetchCronJob',
    'x28.cron.NotificationCronJob',
    'x28.cron.SyncGraphCronJob',
    'django_cron.cron.FailedRunsNotificationCronJob'  # sends notifications for failed jobs
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'request_logging.middleware.LoggingMiddleware',
]

ASGI_APPLICATION = 'chat.routing.application'

ROOT_URLCONF = 'scrambl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scrambl.wsgi.application'

ACCOUNT_ADAPTER = 'users.adapters.ScramblUserAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'users.adapters.ScramblSocialAccountAdapter'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    #'EXCEPTION_HANDLER': 'scrambl.utils.rest_exception_handler.validation_exception_handler'
}

# make sure the correct URLs are used behind a proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER': "users.serializers.ScramblPasswordResetSerializer"
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.ScramblRegisterSerializer'
}


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False


OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

SOCIALACCOUNT_PROVIDERS = {
    'linkedin_oauth2': {
        'SCOPE': [
            'r_liteprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'firstName',
            'lastName',
            'email-address',
            #'geoLocation',
            #'languages',
            #'educations',
            #'projects',
            #'publications',
            #'skills',
        ],
        'VERIFIED_EMAIL': True  # we trust linkedin email verification
    }
}

# Following is added to enable registration with email instead of username
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",

    # per-object permissions using django-guardian
    'guardian.backends.ObjectPermissionBackend'
)

AUTH_USER_MODEL = 'users.ScramblUser'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# used for admin-interface only
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/internal/'


# Allow API access with authentication from frontend
CORS_ORIGIN_WHITELIST = (
    FRONTEND_BASE.strip('/'),
)

# allow access by localhost frontends for development purposes
if bool(os.getenv("DJANGO_ALLOW_LOCALHOST_FRONTEND", False)):
    CORS_ORIGIN_WHITELIST += (
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    )

CORS_EXPOSE_HEADERS = [
    'Content-Disposition',  # important for static file downloads via API to tell the frontend the filename
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'sentry-trace',
]

EMAIL_BACKEND = "mail.backend.ScramblMailerBackend"

# TODO: fix. only needed for chat authentication
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamp': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'timestamp'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',  # change debug level as appropiate
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'DEBUG' if (DEBUG and LOG_QUERIES) else 'INFO',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}

# Allows modals in admin_interface to use frames
X_FRAME_OPTIONS = 'SAMEORIGIN'

# disable ANSI-color in logging (important if logging to file)
REQUEST_LOGGING_ENABLE_COLORIZE=False

if SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            AioHttpIntegration(),
            RedisIntegration()
        ],
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=SENTRY_DEFAULT_PII
    )

# 300% of allowed size to enable attachment-app to give a proper error.
# django return http 400 if max memory size is exceeded
DATA_UPLOAD_MAX_MEMORY_SIZE = ATTACHMENT_MAX_SIZE * 1024 * 1024 * 3


# Allowed attachment mimetypes
ATTACHMENT_TYPES = [
    'application/pdf',
    'application/zip',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'image/jpeg',
    'image/png',
    'text/rtf'
]

CONTRACT_UPLOAD_TYPES = [
    'application/pdf',
    'image/png',
    'image/jpeg',
]

ID_CARD_UPLOAD_TYPES = [
    'application/pdf',
    'image/png',
    'image/jpeg',
]


# contract pdf generation
pdfmetrics.registerFont(TTFont('CalibriBold', os.path.join(BASE_DIR, 'scrambl/fonts/calibrib.ttf')))
pdfmetrics.registerFont(TTFont('Calibri', os.path.join(BASE_DIR, 'scrambl/fonts/calibri.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat', os.path.join(BASE_DIR, 'scrambl/fonts/Montserrat-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Light', os.path.join(BASE_DIR, 'scrambl/fonts/Montserrat-Light.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', os.path.join(BASE_DIR, 'scrambl/fonts/Montserrat-Bold.ttf')))
CONTRACT_TEMPLATE = os.path.join(MEDIA_ROOT, 'templates/flexworker.pdf')
CONTRACT_PAGE_SIZE = A4
CONTRACT_FONT = 'Montserrat-Light'
CONTRACT_FONT_SIZE = 10
CONTRACT_LINE_HEIGHT = 15
CONTRACT_NAME_X_POS = 72
CONTRACT_NAME_Y_POS = 503
CONTRACT_CENTER_TEXT = False

SUMMERNOTE_CONFIG = {
    'disable_attachment': False,

    'summernote': {
        # As an example, using Summernote Air-mode
        #'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '480',

        # Use proper language setting automatically (default)
        #'lang': None,

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            #['fontname', ['fontname']],
            #['color', ['color']],
            ['para', ['ul', 'ol']],
            #['table', ['table']],
            #['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview']],
        ],

        'styleTags': [
            'p', 'h1', 'h4'
        ],

        # Or, explicitly set language/locale for editor
        #'lang': 'ko-KR',

    },

    'css': (
        '/static/internal/css/summernote-custom.css',
    ),

}