# -*- coding: utf-8 -*-
from django.conf.urls import patterns


urlpatterns = patterns('processo.views',
                       (r'processos/(?P<pdf>\d)$', 'processos'),
                       (r'processos$', 'processos'),
                       )
