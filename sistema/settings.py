# Django settings for sistema project.

#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Antonio', 'antonio@ansp.br'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'sistema',
        #'USER': 'sistema',
        #'PASSWORD': 'sistema'
    }
}

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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/files'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/files/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/lib/sistema/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django.core.context_processors.media',
    'django.core.context_processors.static', 
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages', 
    'utils.context_processors.applist',
    'utils.context_processors.debug',
    'utils.context_processors.papelaria',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'ckeditor',
    'import_export',
    'treemenus',
    'menuextension'
)

PROJECT_APPS = (
    'carga',
    'configuracao',
    'evento',
    'financeiro',
    'identificacao',
    'membro',
    'memorando',
    'monitor',
    'outorga',
    'patrimonio',
    'pesquisa',
    'processo',
    'protocolo',
    'rede',
    'verificacao',
    'repositorio',
    'utils',
)
INSTALLED_APPS += PROJECT_APPS

#############################################################
INSTALLED_APPS += (
    'django_cas_ng',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
    'middleware.SSLRedirect',
    'utils.request_cache.RequestCacheMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

CAS_SERVER_URL = 'https://cas.ansp.br/cas/'
CAS_VERSION = '1'
CAS_LOGOUT_COMPLETELY = True
## end django_cas settings

# Faz com que os cookies sejam descartados quando o browser for fechado
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1200
SESSION_SAVE_EVERY_REQUEST = True

LOGIN_REDIRECT_URL = '/'

SERVER_EMAIL='sistema@ansp.br'

#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#EMAIL_HOST='gmail-smtp-in.l.google.com'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='nara@ansp.br'
EMAIL_HOST_PASSWORD='1234'
EMAIL_USE_TLS=True


STATIC_ROOT = '/var/www/media/'
STATIC_URL = '/media/'

TINYMCE_JS_URL='/media/js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG={'theme':'advanced', 'plugins': 'table,style', 'theme_advanced_buttons3_add_before' : 'styleprops,tablecontrols,separator', 'height':80}


CKEDITOR_UPLOAD_PATH='/var/www/files/ckeditor'
