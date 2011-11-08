# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('isms.views',
    (r'atualiza$', 'atualiza'),
    (r'atualiza_old$', 'atualiza1'),
    (r'evals$', 'evals'),
    (r'^$', 'index'),
)


