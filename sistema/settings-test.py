from settings import *

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'blablabla'


TEMPLATE_DIRS += (
    'C:/projetos/workspace/sistema-novo-svn/templates',
    '/var/lib/sistema/templates/',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    }
}

#pip install pyyaml
FIXTURE_DIRS = (
   '/projetos/workspace/sistema-novo-svn/fixtures/',
   '/var/www/fixtures/',
   '/var/lib/jenkins/jobs/sistema-testes/workspace/sistema/fixtures/'
)

STATICFILES_DIRS = (
     '/projetos/workspace/sistema-novo-svn/staticfiles/',
     '/var/www/files/',
     '/var/lib/jenkins/jobs/sistema-testes/workspace/sistema/staticfiles/'
)

STATIC_ROOT = '/var/sistema-novo-svn/staticfiles/'
STATIC_URL = '/files/'


INSTALLED_APPS = (
    'django_jenkins',
) + INSTALLED_APPS



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


# start JENKINS CONFIGURATION
JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
#    'django_jenkins.tasks.django_tests',   # select one django or
 #    'django_jenkins.tasks.dir_tests',      # directory tests discovery
 #    'django_jenkins.tasks.run_pep8',
 #    'django_jenkins.tasks.run_pyflakes',
 #    'django_jenkins.tasks.run_jslint',
 #    'django_jenkins.tasks.run_csslint',    
 #    'django_jenkins.tasks.run_sloccount',    
 #    'django_jenkins.tasks.lettuce_tests',
)
# end JENKINS CONFIGURATION