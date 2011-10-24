from django.conf.urls.defaults import *

urlpatterns = patterns('identificacao.views',
    (r'escolhe_entidade$', 'escolhe_entidade'),
    (r'escolhe_endereco$', 'escolhe_endereco'),
    (r'relatorios/arquivos$', 'arquivos_entidade'),
)

