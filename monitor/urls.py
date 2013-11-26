# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('monitor.views',
    (r'grafico/(?P<link_id>\d+)$', 'grafico'),
    (r'graficos$', 'index'),
)
