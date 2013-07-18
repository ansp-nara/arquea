# Common Django settings for sistema project.
import os

cwd = os.path.dirname(os.path.abspath(__file__)) 
project_path = cwd[:-9] # chop off "settings/"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_cas.middleware.CASMiddleware',
    'middleware.SSLRedirect',
)

ROOT_URLCONF = 'sistema.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % project_path,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django.core.context_processors.media',
    'django.core.context_processors.static', 
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages', 
    'sistema.utils.context_processors.applist',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas',
    'sistema.protocolo',
    'sistema.identificacao',
    'sistema.membro',
    'sistema.outorga',
    'sistema.financeiro',
    'sistema.patrimonio',
    'sistema.memorando',
    'sistema.pesquisa',
    'sistema.questionario',
    'sistema.monitor',
    'sistema.rede',
    'sistema.evento',
    'sistema.processo',
    'tinymce',
    'ckeditor',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://cas.ansp.br/cas/'
CAS_VERSION = '1'
CAS_LOGOUT_COMPLETELY = True


LOGIN_REDIRECT_URL = '/'

SERVER_EMAIL='sistema@ansp.br'


STATICFILES_DIRS = (
     '%s/staticfiles' % project_path,
)

STATIC_URL = '/media/'

TINYMCE_JS_URL='%s/js/tiny_mce/tiny_mce.js' % STATIC_URL
TINYMCE_DEFAULT_CONFIG={'theme':'advanced', 'plugins': 'table,style', 'theme_advanced_buttons3_add_before' : 'styleprops,tablecontrols,separator', 'height':80}

