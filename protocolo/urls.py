# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('protocolo.views',
    (r'^(?P<prot_id>\d+)/cotacoes/$', 'cotacoes'),
    (r'escolhe_termo$', 'escolhe_termo'),
    (r'listagem/(?P<t_id>\d+)$', 'lista_protocolos'),
    (r'protocolos/(?P<termo_id>\d+)$', 'protocolos'),
    (r'descricao$', 'protocolos_descricao'),
    (r'descricao/(?P<pdf>\d)$', 'protocolos_descricao'),
)
