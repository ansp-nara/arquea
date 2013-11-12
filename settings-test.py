from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = 'blablabla'


INSTALLED_APPS += (
    'django_jenkins',
)

STATICFILES_DIRS = (
     '/projetos/workspace/sistema/staticfiles/',
     '/var/www/files/',
)

STATIC_ROOT = '/projetos/workspace/sistema/media/'
STATIC_URL = '/media/'
MEDIA_URL = '/files/'
MEDIA_ROOT = '/var/www/files/'
ADMIN_MEDIA_PREFIX = '/media/'



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
PROJECT_APPS = (
    'sistema.carga',
    'sistema.evento',
    'sistema.financeiro',
    'sistema.identificacao',
    'sistema.membro',
    'sistema.memorando',
    'sistema.monitor',
    'sistema.outorga',
    'sistema.patrimonio',
    'sistema.pesquisa',
    'sistema.processo',
    'sistema.protocolo',
    'sistema.questionario',
    'sistema.rede',
    'sistema.verificacao',
)

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',   # select one django or
 #    'django_jenkins.tasks.dir_tests',      # directory tests discovery
 #    'django_jenkins.tasks.run_pep8',
 #    'django_jenkins.tasks.run_pyflakes',
 #    'django_jenkins.tasks.run_jslint',
 #    'django_jenkins.tasks.run_csslint',    
 #    'django_jenkins.tasks.run_sloccount',    
 #    'django_jenkins.tasks.lettuce_tests',
)



# end JENKINS CONFIGURATION