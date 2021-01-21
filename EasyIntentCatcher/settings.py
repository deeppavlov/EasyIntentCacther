"""
Django settings for EasyIntentCatcher project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
# here is coommon settings
# WARNING you need to create a local.py file with private settings and specify SECRET_KEY there
import os

try:
    from .secret_key import SECRET_KEY
except ImportError:
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    from django.core.management.utils import get_random_secret_key
    sec_key = get_random_secret_key()
    with open(f'{SETTINGS_DIR}/secret_key.py', "w") as sec_key_file:
        sec_key_file.write(f"SECRET_KEY='{sec_key}'")
    # generate_secret_key(os.path.join(, 'secret_key.py'))
    from .secret_key import SECRET_KEY


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "*.*.*.*",
    # TODO del me
    "93.175.20.219",
    "192.168.10.168",

]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',

    'constance.backends.database',
    # 'constance',
    'prediction_models.apps.IntentCactherConstance',
    'ic_dataset',
    'predictions_log',
    'prediction_models',

 ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EasyIntentCatcher.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # TODO dirs in rel path
            'ic_dataset/templates/admin',
            'ic_dataset/templates',
            'templates',
            'templates/admin',

            # '/home/alx/Cloud/aiml_related/EasyIntentCatcher/ic_dataset/templates/admin',
            # '/home/alx/Cloud/aiml_related/EasyIntentCatcher/ic_dataset/templates',
            # '/home/alx/Cloud/aiml_related/EasyIntentCatcher/templates',
            # '/home/alx/Cloud/aiml_related/EasyIntentCatcher/templates/admin',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'EasyIntentCatcher.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

CELERY_BROKER='redis://localhost:6379/0'
CELERY_BROKER_URL='redis://localhost:6379/0'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# restricts number of phrases you can attach to intent:
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240


# Configs App:
CONSTANCE_SUPERUSER_ONLY = False

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'SSH_EXPORT_MODELS': (False, "Enable models exporting to SSH server", bool),
    'SSH_HOST': ('', 'SSH Host for models export'),
    'SSH_USERNAME': ('', 'Username for SSH export'),
    'SSH_PASSWORD': ('', 'Password for SSH export', 'password_input_field'),
    'SSH_PORT': (22, 'SSH Port', int),
    'SSH_EXPORT_TARGET_BASE_PATH': ("/home/export/intent_catcher/", 'directory path for exported models on SSH server')
}

CONSTANCE_CONFIG_FIELDSETS = {
    'SSH Export Options': ('SSH_EXPORT_MODELS',
                        'SSH_HOST', 'SSH_PORT', 'SSH_USERNAME', 'SSH_PASSWORD', 'SSH_EXPORT_TARGET_BASE_PATH'),
    # 'Theme Options': ('THEME',),
}

CONSTANCE_ADDITIONAL_FIELDS = {
    'password_input_field': ['django.forms.fields.CharField', {
        'widget': 'django.forms.PasswordInput',
        'widget_kwargs': {"render_value": True},
    }],
}
