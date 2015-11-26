# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('abuse.views',
                       (r'tabela/(?P<ano>\d+)/(?P<mes>\d+)$', 'tabela'),
                       (r'grafico$', 'grafico'),
                       )
