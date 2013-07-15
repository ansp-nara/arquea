from django.conf.urls.defaults import *

urlpatterns = patterns('patrimonio.views',
    (r'escolhe_termo$', 'escolhe_termo'),
    (r'escolhe_protocolo$', 'escolhe_protocolo'),
    (r'escolhe_pagamento$', 'escolhe_pagamento'),
    (r'escolhe_entidade$', 'escolhe_entidade'),
    (r'escolhe_patrimonio$', 'escolhe_patrimonio'),
    (r'escolhe_detalhe$', 'escolhe_detalhe'),
    (r'filtra_pn_estado$', 'filtra_pn_estado'),
    (r'patrimonio_existente$', 'patrimonio_existente'),
    (r'relatorio/por_estado$', 'por_estado'),
    (r'relatorio/por_tipo$', 'por_tipo'),
    (r'relatorio/por_marca$', 'por_marca'),
    (r'relatorio/por_marca/(?P<pdf>\d)$', 'por_marca'),
    (r'relatorio/por_local$', 'por_local'),
    (r'relatorio/por_local/(?P<pdf>\d)$', 'por_local'),
    (r'relatorio/por_termo$', 'por_termo'),
    (r'relatorio/por_termo/(?P<pdf>\d)$', 'por_termo'),
    (r'relatorio/por_tipo_equipamento$', 'por_tipo_equipamento'),
    (r'relatorio/por_tipo_equipamento2$', 'por_tipo_equipamento2'),
    (r'relatorio/presta_contas$', 'presta_contas'),
    (r'abre_arvore$', 'abre_arvore'),
    (r'abre_arvore_tipo$', 'abre_arvore_tipo'),
    (r'racks$', 'racks'),
)

