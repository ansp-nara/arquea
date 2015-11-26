# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('identificacao.views',
                       (r'escolhe_entidade$', 'ajax_escolhe_entidade'),
                       (r'escolhe_endereco$', 'ajax_escolhe_endereco'),
                       (r'escolhe_entidade_filhos$', 'ajax_escolhe_entidade_filhos'),
                       (r'relatorios/arquivos$', 'arquivos_entidade'),
                       (r'agenda/(?P<pdf>[a-z]+)/(?P<tipo>\d+)$', 'agenda'),
                       (r'agenda/(?P<pdf>[a-z]+)$', 'agenda'),
                       (r'agenda/(?P<tipo>\d+)/$', 'agenda'),
                       (r'agenda$', 'agenda'),
                       (r'acessos/terremark$', 'acessos_terremark'),
                       (r'ecossistema/(?P<tipo>[a-z]+)$', 'planilha_ecossistema'),
                       )
