from django.conf.urls.defaults import *

urlpatterns = patterns('outorga.views',
#    (r'^termo/(?P<termo_id>\d+)/$', 'termo'),
#    (r'^pedido/(?P<pedido_id>\d+)/$', 'pedido'),
#    (r'escolhe_termo$', 'escolhe_termo'),
#    (r'escolhe_modalidade$', 'escolhe_modalidade'),
#    (r'seleciona_termo_natureza$', 'seleciona_termo_natureza'),
#    (r'seleciona_mod_item_natureza$', 'seleciona_mod_item_natureza'),
#    (r'seleciona_item_natureza$', 'seleciona_item_natureza'),
    (r'relatorios/acordos$', 'gastos_acordos'),
    (r'relatorios/contratos$', 'contratos'),
    (r'relatorios/por_item$', 'por_item'),
    (r'relatorios/termos$', 'relatorio_termos'),
)
