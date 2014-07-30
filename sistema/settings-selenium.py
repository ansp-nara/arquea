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
INSTALLED_APPS += (
    'django_jenkins',
#    'selenium_tests',
)

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
#     'django_jenkins.tasks.django_tests',   # select one django or
 #    'django_jenkins.tasks.dir_tests',      # directory tests discovery
 #    'django_jenkins.tasks.run_pep8',
 #    'django_jenkins.tasks.run_pyflakes',
 #    'django_jenkins.tasks.run_jslint',
 #    'django_jenkins.tasks.run_csslint',    
 #    'django_jenkins.tasks.run_sloccount',    
 #    'django_jenkins.tasks.lettuce_tests',
)

PROJECT_APPS = (
                'selenium_tests',
                
                )

#JENKINS_TEST_RUNNER = 'django_selenium.jenkins_runner.JenkinsTestRunner'
TEST_RUNNER = 'django_selenium.selenium_runner.SeleniumTestRunner'
#JENKINS_TEST_RUNNER = 'django_selenium.selenium_runner.SeleniumTestRunner'

# end JENKINS CONFIGURATION


# start SELENIUM CONFIGURATION


# host do selenium server
# SELENIUM_HOST = 'localhost'
# # port do selenium server
# SELENIUM_PORT = '4444'
# # host do sistema a ser testado
# SELENIUM_SISTEMA_HOST ='10.2.0.150:8000'


# host do selenium server
SELENIUM_HOST = '10.0.0.23'
# port do selenium server
SELENIUM_PORT = 4443

SELENIUM_TESTSERVER_HOST ='10.0.0.23'

# host do sistema a ser testado
SELENIUM_SISTEMA_HOST ='10.0.0.23'

SELENIUM_SISTEMA_USERNAME ='teste'

SELENIUM_SISTEMA_PASS ='selenium135#%&'

SELENIUM_DRIVER = 'Remote'
# end SELENIUM CONFIGURATION

