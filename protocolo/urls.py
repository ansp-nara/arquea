# -*- coding: utf-8 -*-

from django.conf.urls import patterns


urlpatterns = patterns('protocolo.views',
                       (r'^(?P<prot_id>\d+)/cotacoes/$', 'cotacoes', None, 'cotacoes'),
                       (r'escolhe_termo$', 'escolhe_termo'),
                       # (r'listagem/(?P<t_id>\d+)$', 'lista_protocolos'),
                       (r'descricao$', 'protocolos_descricao'),
                       (r'descricao/(?P<pdf>\d)$', 'protocolos_descricao'),
                       )