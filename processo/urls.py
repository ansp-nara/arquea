from django.conf.urls.defaults import *

urlpatterns = patterns('processo.views',
    (r'processos/(?P<pdf>\d)$', 'processos'),
    (r'processos$', 'processos'),
)

