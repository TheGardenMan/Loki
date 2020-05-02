# Heroku tut.. https://blog.usejournal.com/deploying-django-to-heroku-connecting-heroku-postgres-fcc960d290d1
import os
import django_heroku
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

template_loc=BASE_DIR+'/templates'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static')# Where to save uploaded files.

LOGIN_URL = '/login/'
# Since testing,we're serving static files using django
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!87tyzawm(9r+9kpz6!*94u^ey#!f+onqv4b0@ov=rdcrvnhmf'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #Please see below
# 		ENCRYPTED COOKIES:EXTERNAL MODULE
# https://github.com/brightinteractive/django-encrypted-cookie-session
# SESSION_ENGINE = 'encrypted_cookies'
# ToDo change this during to true  production (assuming we're using HTTPS in production.We should.) ref::# https://github.com/brightinteractive/django-encrypted-cookie-session
# SESSION_COOKIE_SECURE = False
# ENCRYPTED_COOKIE_KEYS = ['GawfJ8vItYYACr6sor9f5XMki-SnN2rZ-uI0ykcainU=']
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'LokiApp',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'LokiProject.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [template_loc],
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

WSGI_APPLICATION = 'LokiProject.wsgi.application'

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# Do not comment this asshole
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'postgres',
		'USER': 'postgres',
		'PASSWORD': 'jaxtek',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)

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
django_heroku.settings(locals())
