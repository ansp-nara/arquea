from settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/files/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r(^k*hs*17sjna7i*(fs75=^_r$3(i!r*yok$(n6g61*3s_x3j'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'C:/projetos/workspace/sistema/templates',
)

CKEDITOR_UPLOAD_PATH='/tmp/ckeditor'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'sistema',
        'USER': 'sistema-user',
        'PASSWORD': '1234'
    }
}
          
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='nara@ansp.br'
EMAIL_HOST_PASSWORD='1234'
EMAIL_USE_TLS=True

STATICFILES_DIRS = (
     'C:/projetos/workspace/sistema/staticfiles/',
)
STATIC_ROOT = '/var/www/media/'
STATIC_URL = '/media/'


INSTALLED_APPS += (
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] %(name)s.%(funcName)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False
        },
    }
}


