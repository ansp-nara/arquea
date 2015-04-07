from settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/files/'
MEDIA_ROOT = '/var/www/files/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'blablabla'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/antonio/develop/sistema/templates',
)

CKEDITOR_UPLOAD_PATH='ckeditor/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/antonio/develop/db.django', 
#         'HOST': '10.0.0.97',
#         'NAME': 'rogerio',
#         'USER': 'rogerio',
#         'PASSWORD': 'sistema'

    }
}
          
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='nara@ansp.br'
EMAIL_HOST_PASSWORD='1234'
EMAIL_USE_TLS=True

STATICFILES_DIRS = (
     '/home/antonio/develop/sistema/staticfiles/',
     '/var/www/files/',
)

STATIC_ROOT = '/tmp/media/'
STATIC_URL = '/media/'


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


JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',   # select one django or
    #'django_jenkins.tasks.dir_tests'      # directory tests discovery
#    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
#    'django_jenkins.tasks.run_jslint',
#    'django_jenkins.tasks.run_csslint',    
    'django_jenkins.tasks.run_sloccount',    
#    'django_jenkins.tasks.lettuce_tests',
)


WKHTMLTOPDF_CMD = 'C:/Program Files (x86)/wkhtmltopdf/wkhtmltopdf.exe'
WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': True,
    # Para o Linux, descomentar esta linha
    # 'zoom':0.63,
}
