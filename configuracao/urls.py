# -*- coding: utf-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('configuracao.views',
                       (r'^help/(\w+)/(\w+)/$', 'help_text'),
                       (r'^tooltip/(\w+)/(\w+)$', 'tooltip'),
                       (r'^has_help/(\w+)/(\w+)/$', 'has_help_text')
                       )
