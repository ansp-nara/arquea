from django.conf.urls import *

urlpatterns = patterns('identificacao.views',
    (r'escolhe_entidade$', 'escolhe_entidade'),
    (r'escolhe_endereco$', 'escolhe_endereco'),
    (r'escolhe_entidade_filhos$', 'escolhe_entidade_filhos'),
    (r'relatorios/arquivos$', 'arquivos_entidade'),
    (r'agenda/(?P<pdf>[a-z]+)/(?P<tipo>\d+)$', 'agenda'),
    (r'agenda/(?P<pdf>[a-z]+)$', 'agenda'),
    (r'agenda/(?P<tipo>\d+)/$', 'agenda'),
    (r'agenda$', 'agenda'),
    (r'acessos/terremark$', 'acessos_terremark'),
    (r'ecossistema/(?P<tipo>[a-z]+)$', 'planilha_ecossistema'),
)

