from django.conf.urls.defaults import *

urlpatterns = patterns('rede.views',
    (r'escolhe_pagamento$', 'escolhe_pagamento'),
    (r'planejamento$', 'planejamento'),
    (r'planejamento2$', 'planejamento2'),
    (r'planejamento/(?P<pdf>\d)$', 'planejamento'),
    (r'planejamento2/(?P<pdf>\d)$', 'planejamento2'),
    (r'info$', 'planilha_informacoes_gerais'),
    (r'info.pdf$', 'imprime_informacoes_gerais'),
    (r'info_tec/(?P<id>\d+)$', 'planilha_informacoes_tecnicas'),
    (r'blocosip', 'blocos_ip'),
    (r'blocos.txt', 'blocos_texto'),
    (r'planeja_contrato$', 'planeja_contrato'),
    (r'custo_terremark$', 'custo_terremark'),
    (r'custo_terremark/(?P<pdf>\d)$', 'custo_terremark'),
)

