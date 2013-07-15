# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('financeiro.views',
    #(r'filtra_modalidade$', 'filtra_modalidade'),
    #(r'escolhe_termo$', 'escolhe_termo'),
    #(r'soma_valor_descricao$', 'soma_valor_descricao'),
    #(r'despesas_auditoria_fapesp$', 'despesas_auditoria_fapesp'),
    #(r'seleciona_origem_fapesp$', 'seleciona_origem_fapesp'),
    #(r'seleciona_outras_origens$', 'seleciona_outras_origens'),
    #(r'seleciona_extrato$', 'seleciona_extrato'),
    #(r'seleciona_identificacao$', 'seleciona_identificacao'),
    (r'pagamento_termo$', 'termo_escolhido'),
    (r'pagamento_numero$', 'numero_escolhido'),
    (r'pagamento_cc$', 'codigo_escolhido'),
    (r'parcial_pagina_termo$', 'parcial_pagina'),
    (r'nova_pagina$', 'nova_pagina'),
    (r'relatorios/pagamentos_mes$', 'pagamentos_mensais'),
    (r'relatorios/pagamentos_parcial$', 'pagamentos_parciais'),
    (r'relatorios/pagamentos_parcial/(?P<pdf>\d)$', 'pagamentos_parciais'),
    (r'relatorios/gerencial$', 'relatorio_gerencial'),
    (r'relatorios/gerencial/(?P<pdf>\d)$', 'relatorio_gerencial'),
    (r'relatorios/acordos$', 'relatorio_acordos'),
    (r'relatorios/acordos/(?P<pdf>\d)$', 'relatorio_acordos'),
    (r'relatorios/parciais$', 'parciais'),
    (r'relatorios/caixa$', 'parciais', {'caixa':True}),
    (r'relatorios/prestacao$', 'presta_contas'),
    (r'relatorios/prestacao/(?P<pdf>\d)$', 'presta_contas'),
    (r'relatorios/tipos$', 'tipos_documentos'),
    (r'cheque/(?P<cc>\d+)$', 'cheque'),
    (r'^extrato$', 'extrato'),
    (r'^extrato/(?P<pdf>\d)$', 'extrato'),
    (r'extrato_tarifas$', 'extrato_tarifas'),
    (r'extrato_mes$', 'extrato_mes'),
    (r'extrato_financeiro$', 'extrato_financeiro'),
    (r'extrato_financeiro_parciais$', 'financeiro_parciais'),
    (r'sel_extrato$', 'escolhe_extrato'),
    (r'extrato_financeiro_parciais/(?P<pdf>\d+)$', 'financeiro_parciais'),
    #(r'relatorio/(?P<termo>\d+)/(?P<modalidade>\d+)$', 'relatorio_despesas'),
    #(r'relatorio/(?P<termo>\d+)$', 'relatorio_despesas'),
    #(r'relatorio$', 'relatorio_despesas'),
    #(r'relatorio\.pdf/(?P<termo>\d+)/(?P<modalidade>\d+)$', 'relatorio_despesas', {'pdf':True}),
    #(r'relatorio\.pdf/(?P<termo>\d+)$', 'relatorio_despesas', {'pdf':True}),
    #(r'relatorio\.pdf$', 'relatorio_despesas', {'pdf':True}),
)
