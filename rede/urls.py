from django.conf.urls import *

urlpatterns = patterns('rede.views',
    (r'escolhe_pagamento$', 'ajax_escolhe_pagamento'),
    (r'planejamento$', 'planejamento'),
    (r'planejamento2$', 'planejamento2'),
    (r'planejamento/(?P<pdf>\d)$', 'planejamento'),
    (r'planejamento2/(?P<pdf>\d)$', 'planejamento2'),
    (r'info$', 'planilha_informacoes_gerais'),
    (r'info.pdf$', 'imprime_informacoes_gerais'),
    (r'info_tec/(?P<id>\d+)$', 'planilha_informacoes_tecnicas'),
    
    (r'blocosip_transito$', 'blocosip_transito'),
    (r'blocosip_inst_transito$', 'blocosip_inst_transito'),
    (r'blocosip_inst_ansp$', 'blocosip_inst_ansp'),
    (r'blocosip_ansp$', 'blocosip_ansp'),
    (r'blocosip$', 'blocosip'),
    
    (r'crossconnection$', 'crossconnection'),
    
    (r'blocos.txt', 'blocos_texto'),
    (r'planeja_contrato$', 'planeja_contrato'),
    (r'custo_terremark$', 'custo_terremark'),
    (r'custo_terremark/(?P<pdf>\d)$', 'custo_terremark'),
    (r'relatorio_recursos_operacional$', 'relatorio_recursos_operacional'),
)


