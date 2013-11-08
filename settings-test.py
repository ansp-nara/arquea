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
