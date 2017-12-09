
# Util
import os
from os import mkdir
from os.path import abspath, basename, dirname, join, normpath, exists
from sys import path


##################################################################################################
########################################## DJANGO CONFIGURATION
##################################################################################################
### These are parameters that Django requires to run

########## TEST CONFIGURATION
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
########## END TEST CONFIGURATION


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)

# Site name:
SITE_NAME = 'rowbot.io'
########## END PATH CONFIGURATION


########## ALLOWED HOSTS CONFIGURATION
ALLOWED_HOSTS = (
  '*',
)
########## END ALLOWED HOSTS CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
  ('Your name', 'youremail@domain.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/London'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## SESSION CONFIGURATION
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
########## END SESSION CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
  normpath(join(DJANGO_ROOT, 'assets')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = '#za#m48_9in&i!9rodpp)r6$4_)_94l0sij7+06&mw6t*9f1t9'
########## END SECRET CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS':{
      'debug':False,
      'context_processors':[
        'django.contrib.auth.context_processors.auth',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.template.context_processors.request',
      ],
    },
    'DIRS':[
      normpath(join(DJANGO_ROOT, 'templates')),
    ],
  },
]
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
  # Use GZip compression to reduce bandwidth.
  'django.middleware.gzip.GZipMiddleware',

  # Default Django middleware.
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'urls'
########## END URL CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## DJANGO APP CONFIGURATION
DJANGO_APPS = (
  # Default Django apps:
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  # Useful template tags:
  'django.contrib.humanize',

  # Admin panel and documentation:
  'django.contrib.admin',
  'django.contrib.admindocs',

  # flatpages for static pages
  'django.contrib.flatpages',
)
########## END DJANGO APP CONFIGURATION


########## FILE UPLOAD CONFIGURATION
FILE_UPLOAD_HANDLERS = (
  'django.core.files.uploadhandler.MemoryFileUploadHandler',
  'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
########## END FILE UPLOAD CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {}
########## END DATABASE CONFIGURATION

##################################################################################################
########################################## END DJANGO CONFIGURATION
##################################################################################################


##################################################################################################
########################################## ROWBOT CONFIGURATION
##################################################################################################
### These are parameters required specifically for ROWBOT


########## APP CONFIGURATION
THIRD_PARTY_APPS = (
  # util
  'rest_framework',
  'rest_framework.authtoken',
)

LOCAL_APPS = (
  'rowbot.apps.RowConfig',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## AUTH CONFIGURATION
AUTH_USER_MODEL = 'rowbot.Member'
########## END AUTH CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    },
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler'
    }
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins', 'console'],
      'level': 'ERROR',
      'propagate': True,
    },
  }
}
########## END LOGGING CONFIGURATION


########## REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication',
  )
}
########## END REST FRAMEWORK CONFIGURATION


########## DATABASE CONFIGURATION
# make local_db directory
DB_ROOT = join(DJANGO_ROOT, 'local_db')
if not exists(DB_ROOT):
  mkdir(DB_ROOT)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': join(DB_ROOT, 'db.sqlite3'),
  }
}
########## END DATABASE CONFIGURATION


########## PASSWORD CONFIGURATION
AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
)

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    'OPTIONS': {
      'min_length': 9,
    }
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]
########## END PASSWORD CONFIGURATION
