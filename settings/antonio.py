ADMINS = (
     ('Antonio', 'antonio@ansp.br'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'sistema',
        'USER': 'sistema',
        'PASSWORD': 'sistema'
    }
}
