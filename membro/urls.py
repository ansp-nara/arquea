from django.conf.urls.defaults import *

urlpatterns = patterns('membro.views',
    (r'controle$', 'controle'),
    (r'mensal/(?P<ano>\d+)/(?P<mes>\d+)$', 'mensal'),
    (r'detalhes$', 'detalhes'),
    (r'obs/(?P<id>\d+)$', 'observacao'),
    (r'mensalf$', 'mensal_func'),
)

