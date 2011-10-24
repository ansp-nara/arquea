from django.conf.urls.defaults import *

urlpatterns = patterns('memorando.views',
    (r'simples/(?P<mem>\d+)$', 'simples'),
    (r'fapesp/(?P<mem>\d+)$', 'fapesp'),
    (r'relatorio/(?P<mem>\d+)$', 'relatorio'),
    (r'relatorio$', 'relatorio'),
    (r'pagamentos$', 'escolhe_pagamentos'),
    (r'perguntas$', 'filtra_perguntas'),
    (r'escolhe_pergunta$', 'escolhe_pergunta'),

)



