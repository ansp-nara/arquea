# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'protocolo'
urlpatterns = [
    url(r'^(?P<prot_id>\d+)/cotacoes/$', views.cotacoes, name='cotacoes'),
    url(r'escolhe_termo$', views.escolhe_termo),
    url(r'descricao$', views.protocolos_descricao),
    url(r'descricao/(?P<pdf>\d)$', views.protocolos_descricao),
    ]