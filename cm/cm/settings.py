"""
Django settings for cm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '61r++_)327va(9v%$4kcg0hlb^2&dea3(^wyo2k8q=3b-smi52'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'cm.models',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cm.urls'

WSGI_APPLICATION = 'cm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(ROOT, "templates")]

DB_HOST = 'localhost'
DB_ENGINE = 'django.db.backends.mysql'
DB_OPTIONS = {'autocommit': True}
DB_USER = 'root'
DB_PORT = 3306

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': 'cm',
        'USER': DB_USER,
        'PASSWORD': 'root',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'cm',
    #     'USER': 'aa',
    #     'PASSWORD': '',
    #     'HOST': '127.0.0.1',
    #     'PORT': '5432',
    #     'OPTIONS': {'autocommit': True},
    # },
}
