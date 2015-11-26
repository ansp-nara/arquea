# -*- coding: utf-8 -*-
from django.conf.urls import patterns


urlpatterns = patterns('memorando.views',
                       (r'simples/(?P<mem>\d+)$', 'simples'),
                       (r'fapesp/(?P<mem>\d+)$', 'fapesp'),
                       (r'relatorio/(?P<mem>\d+)$', 'relatorio'),
                       (r'relatorio$', 'relatorio'),
                       (r'pagamentos$', 'ajax_escolhe_pagamentos'),
                       (r'perguntas$', 'ajax_filtra_perguntas'),
                       (r'escolhe_pergunta$', 'ajax_escolhe_pergunta'),
                       )
